from .Model import Model
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


class TOWTModel(Model):

    def __init__(self, df=None, dependent_col="load",                 
    temperature_col="temp",
                 occupancy_col=None, dependent_df=None, temperature_df=None,
                 additional_vars_df=None, occ_threshold=0.65,
                 knot_temps=[40, 55, 65, 80, 90], define_knot_temps=True,
                 model_name="TOWT"):
        """
        Initialize object by ensuring data provided is fit for modeling and
        noting model specs.
        Parameters
        ----------
        df : Pandas DataFrame, optional
            A preprocessed dataframe that includes a timestamp column,
            dependent variable column, and other regressor variables. No other
            variables should be included. The default is None.
        dependent_col : str, optional
            Needed to mark what the dependent variable will be in the pre-
            processed dataframe. Not used if a preprocessed dataframe is not
            supplied. The default is "load".
        temperature_col : str, optional
            Needed to mark what the temperature variable is in the preprocessed
            dataframe, if a temperature column exists. If one is not needed for
            modeling, input None. Not used if a preprocessed dataframe is not
            supplied. The default is "temp".
        occupancy_col : str, optional
            Needed to mark what the binary occupied variable is in the
            preprocessed dataframe or additional variables dataframe, if a
            occupancy column exists. If one is not supplied, an occupancy
            schedule can be estimated based off the load. If separate
            occupied/unoccupied models are not wanted, change the occ_threshold
            to 1. The default is None.
        dependent_df : Pandas DataFrame, optional
            Dataframe containing a timestamp column and a dependent variable
            column. If wanting to train a model and a preprocessed dataframe
            is not supplied, this is needed. The default is None.
        temperature_df : Pandas DataFrame, optional
            Dataframe containing a timestamp column and a temperature column.
            If the desired model is assuming the dependent variable is
            dependent on temperature, this dataframe is needed. The default is
            None.
        additional_vars_df : Pandas DataFrame, optional
            Dataframe containing a timestamp column and other regressor
            variables. This is merged with the dependent_df dataframe.
            The default is None.
        occ_threshold : float, optional
            Percentage of time assumed to be occupied. The default is 0.65.
        knot_temps : list, optional
            List of knot temperatures for TOWT models. The default is
            [40, 55, 65, 80, 90].
        model_name : str, optional
            Specific model name.
            Options are: TOW, TOWT
            Upper or lower case is accepted. Default is TOWT.

        Returns
        -------
        None.
        """
        super().__init__(df=df,
                         dependent_col=dependent_col,
                         temperature_col=temperature_col,
                         dependent_df=dependent_df,
                         temperature_df=temperature_df,
                         additional_vars_df=additional_vars_df,
                         occupancy_col=occupancy_col,
                         model_name=model_name)
        self.temp_train_cols = []
        self.tow_train_cols = []
        self.occ_threshold = occ_threshold
        self.determined_occ_sched = None
        if self.df is not None:
            self.df = self.df.groupby(self.timestamp_col).mean().reset_index()

        if define_knot_temps:
            self.knot_temps = self.define_kts()
        else:
            self.knot_temps = knot_temps
        if self.model_name not in ["TOWT", "TOW"]:
            raise ValueError("Unknown model type: " + self.model_name + ". "
                             "Please specify model_name as TOW or TOWT.")

    def train(self, interval=None, knot_temps=None):
        """
        Training method for TOWT and TOW model.
        Parameters
        ----------
        model : str, optional
            String that to run either time of week and temperature model or
            just time of week. The default is "TOWT".
        knot_temps : list, optional
            List of knot_temps at least of length 2. Will rewrite class
            knot_temps attribute. The default is None.
        Raises
        ------
        ValueError
            If inferred time interval is monthly, the error will raise.
        Returns
        -------
        Pandas DataFrame
            The main dataframe with all the temp knot and time of week
            variables used for regression attached to it.
        """
        # Checks
        if (knot_temps != self.knot_temps) & (knot_temps is not None):
            self.knot_temps = knot_temps

        if interval is None:
            interval = self.min_interval

        min_available_interval_num = self.interval_tiers[self.min_interval]
        desired_interval_num = self.interval_tiers[interval]

        if min_available_interval_num > desired_interval_num:
            self.df = self.group_interval(time_interval=interval,
                                          time_col=self.timestamp_col)
        self.df.reset_index(drop = True, inplace = True)

        if min_available_interval_num < desired_interval_num:
            raise ValueError(
                'Desired interval: ' + interval +
                ' is unavailable. Highest granularity is ' +
                self.min_interval + '.')

        # Check if time_interval is monthly
        if interval == "Monthly":
            raise ValueError(
                'Inferred time interval is monthly. The TOWT'
                ' algorithm expects hourly or daily data.')

        self.model_interval = interval

        # Define knot temp vars and tow vars
        used_knot_temps = pd.DataFrame()
        temp_vars = pd.DataFrame()
        self.x_train_cols = list(set(self.x_train_cols)
                                 - set(self.temp_train_cols
                                       + self.tow_train_cols))
        if self.model_name == "TOWT":
            temp_vars, used_knot_temps = self.define_temp_vars(
                self.df, self.knot_temps)
            self.temp_train_cols = list(temp_vars.columns)
            self.x_train_cols = self.x_train_cols + self.temp_train_cols
        tow_vars = self.define_tow_vars(self.df, self.model_interval)
        self.tow_train_cols = list(tow_vars.columns)
        self.x_train_cols = self.x_train_cols + self.tow_train_cols

        # Assemble regression datasets
        if self.occupancy_col is None:
            self.df = self.find_occ_unocc(
                time_interval=self.model_interval,
                occ_threshold=self.occ_threshold)
            self.occupancy_col = 'occ'
            self.df.reset_index(drop = True, inplace = True)
            if self.df[self.occupancy_col].nunique() == 1:
                self.df[self.occupancy_col] = 1
            #occ_sched = self.df[[self.timestamp_col, self.occupancy_col]]
        main = pd.concat([self.df, temp_vars, tow_vars], axis=1)
        train = main.dropna().copy()
        # Create models and predict
        # Occupied model
        occ_x_train = train.loc[train[self.occupancy_col]
                                == 1, self.x_train_cols].copy()
        occ_y_train = train.loc[train[self.occupancy_col]
                                == 1, self.dependent_col].copy()
        occ_check = occ_x_train.loc[:, tow_vars.columns].sum() != 0
        occ_x_train[occ_check.index[occ_check].tolist()[0]] = 0
        zero_check = occ_x_train.loc[:, tow_vars.columns].sum() == 0
        occ_x_train.drop(columns=zero_check.index[zero_check].tolist(),
                         inplace=True)
        occ_model = LinearRegression().fit(occ_x_train, occ_y_train)
        self.occ_model = occ_model

        # Unoccupied model
        if train[self.occupancy_col].nunique() > 1:
            unocc_x_train = train.loc[train[self.occupancy_col]
                                      == 0, self.x_train_cols].copy()
            unocc_y_train = train.loc[train[self.occupancy_col]
                                      == 0, self.dependent_col].copy()
            unocc_check = unocc_x_train.loc[:, tow_vars.columns].sum() != 0
            unocc_x_train[unocc_check.index[unocc_check].tolist()[0]] = 0
            zero_check = unocc_x_train.loc[:, tow_vars.columns].sum() == 0
            unocc_x_train.drop(columns=zero_check.index[zero_check].tolist(),
                               inplace=True)
            unocc_model = LinearRegression().fit(unocc_x_train, unocc_y_train)
            self.unocc_model = unocc_model

        return(main)

    def predict(self, df):
        """
        Predict method for TOWT and TOW models.
        Parameters
        ----------
        df : Pandas DataFrame
            Dataframe consisting of at least time['time'] and occupancy['occ'].
            Temp is needed for TOWT.

        Returns
        -------
        The main pandas dataframe with the predictions attached to it.
        """

        # Check if time_interval is monthly
        if self.model_interval == "Monthly":
            raise ValueError(
                'Inferred time interval is monthly. The TOWT'
                ' algorithm expects hourly or daily data.')

        # Define knot temp vars and tow vars
        used_knot_temps = pd.DataFrame()
        temp_vars = pd.DataFrame()
        if self.model_name == "TOWT":
            temp_vars, used_knot_temps = self.define_temp_vars(
                df, self.knot_temps)
        tow_vars = self.define_tow_vars(df, self.model_interval)

        main = pd.concat([df, temp_vars, tow_vars], axis=1)
        pred = main.dropna().copy()
        # Fill in occ sched based off trained model if occ not supplied
        if self.determined_occ_sched is not None:
            if self.model_interval.upper()=="DAILY":
                tow = pred[self.timestamp_col].dt.dayofweek
                pred[self.occupancy_col] = tow.replace(self.determined_occ_sched)
            elif self.model_interval.upper()=="HOURLY":
                dow = pred[self.timestamp_col].dt.dayofweek
                hour = pred[self.timestamp_col].dt.hour
                tow = dow*24+hour
                pred[self.occupancy_col] = tow.replace(self.determined_occ_sched)
            if pred[self.occupancy_col].nunique() == 1:
                pred[self.occupancy_col] = 1
                
        if self.model_name == "TOWT":
            pred.drop(columns=['time', 'temp'], inplace=True)
        else:
            pred.drop(columns=['time'], inplace=True)
        
        
        # Predict
        occ_x_pred = pd.DataFrame()
        unocc_x_pred = pd.DataFrame()
        if 1 in pred[self.occupancy_col].unique():
            occ_x_pred = pred.loc[pred[self.occupancy_col] == 1,
                                  pred.columns != self.dependent_col]
            occ_x_pred.drop(columns=self.occupancy_col, inplace=True)
            occ_x_pred = occ_x_pred.loc[:, self.occ_model.feature_names_in_]
            occ_x_pred['predict'] = self.occ_model.predict(occ_x_pred)
        if 0 in pred[self.occupancy_col].unique():
            unocc_x_pred = pred.loc[pred[self.occupancy_col] == 0,
                                    pred.columns != self.dependent_col]
            unocc_x_pred.drop(columns=self.occupancy_col, inplace=True)
            unocc_x_pred = unocc_x_pred.loc[:,
                                            self.unocc_model.feature_names_in_]
            unocc_x_pred['predict'] = self.unocc_model.predict(unocc_x_pred)

        pred = pd.concat([occ_x_pred, unocc_x_pred], axis=0)
        out = pd.concat([df, pred['predict']], axis=1)
        return(out)

    def temp0(self, temp, knot_temp):
        """
        Defining first knot temp values in TOWT model.
        Parameters
        ----------
        temp : float
            Temperature value from the 'temp' column in the main dataframe.
        knot_temp : float
            The lowest knot temp.
        Returns
        -------
        float
            The first knot temperature variable value for TOWT model.
        """

        if temp > knot_temp:
            return(knot_temp)
        else:
            return(temp)

    def tempi(self, temp, knot_tempi, knot_tempj):
        """
        Defining the middle knot temp values in TOWT model.
        Parameters
        ----------
        temp : float
            Temperature value from the 'temp' column in the main dataframe.
        knot_tempi : float
            A knot temperature that is not the lowest or greatest.
        knot_tempj : float
            A knot temperature that is one index lower than i
        Returns
        -------
        float
            A middle knot temperature variable value in the TOWT model.
        """

        if temp > knot_tempi:
            return(knot_tempi - knot_tempj)
        else:
            if temp > knot_tempj:
                return(temp - knot_tempj)
            else:
                return(0)

    def tempn(self, temp, knot_tempn):
        """
        Defining the last knot temp value in TOWT model.
        Parameters
        ----------
        temp : float
            Temperature value from the 'temp' column in the main dataframe.
        knot_tempn : float
            The highest knot temperature.
        Returns
        -------
        float
            The last knot temperature variable value.
        """
        if temp > knot_tempn:
            return(temp - knot_tempn)
        else:
            return(0)

    def define_temp_vars(self, df, knot_temps):
        """
        Define all knot temperature variable values given a dataframe with
        temperature and specific knot temperatures.
        Parameters
        ----------
        df : pandas dataframe
            The main pandas dataframe that will be used for analysis with a
            numeric temperature column.
        knot_temps : list
            List of specific knot temperatures.
        Returns
        -------
        towt_vars: Pandas DataFrame
            Dataframe consisting of the TOWT variables.
        knot_temps : TYPE
            Used knot temperatues to determine TOWT variables.
        """
        # Define min and max temperatures in dataset
        min_temp = df['temp'].min()
        max_temp = df['temp'].max()

        # Drop outside knot temperature bounds if redundant
        # knot_temps = [x for x in knot_temps if x > min_temp]
        # knot_temps = [x for x in knot_temps if x < max_temp]

        # Sort knot temperatures from least to greatest
        knot_temps.sort()

        # Create the temperature variables according to LBNL algo (Mathieu)
        temp_var_dict = {}
        for i in range(len(knot_temps)):
            idx = 'temp'+str(i)
            if i == 0:
                temp_var_dict[idx] = df['temp'].apply(
                    self.temp0, args=(knot_temps[i],)).values
            elif i == len(knot_temps)-1:
                temp_var_dict[idx] = df['temp'].apply(
                    self.tempi, args=(knot_temps[i], knot_temps[i-1])).values
                temp_var_dict['temp'+str(i+1)] = df['temp'].apply(self.tempn,
                                                                  args=(knot_temps[i],)).values
            else:
                temp_var_dict[idx] = df['temp'].apply(
                    self.tempi, args=(knot_temps[i], knot_temps[i-1])).values

        return pd.DataFrame(temp_var_dict), knot_temps
    
    def define_kts(self, n_chunks=6):
        temp_array = np.copy(self.df[self.temperature_col].values)
        temp_array = np.array_split(np.unique(np.sort(temp_array)), n_chunks)
        kts = []
        for i in range(len(temp_array)-1):
            kt = (temp_array[i].max() + temp_array[i+1].min())/2
            kts.append(kt)
        
        return(kts)
        

    @staticmethod
    def define_tow_vars(df, time_interval):
        """
        The function creates time of week indicator variables. 168 hours of
        week or 7 days of week.
        Parameters
        ----------
        df : Pandas DataFrame
            Dataframe consisting of at a minimum a timestamp column labelled
            "time".
        time_interval : str
            DESCRIPTION.
        Returns
        -------
        Pandas DataFrame
            Dataframe containing indicator variables for time of week.
        """
        if time_interval.upper() == 'DAILY':
            out_init = pd.DataFrame(0, index=np.arange(df.shape[0]),
                                    columns=['tow_'+str(x) for x in range(7)])
            dow = df['time'].dt.dayofweek
            tow_vars = pd.get_dummies(dow, prefix="tow")
            out_init.loc[:, tow_vars.columns] = tow_vars
            return(out_init)

        elif time_interval.upper() == 'HOURLY':
            out_init = pd.DataFrame(0, index=np.arange(df.shape[0]),
                                    columns=['tow_'+str(x) for x in range(168)])
            dow = df['time'].dt.dayofweek
            hour = df['time'].dt.hour
            tow = dow*24 + hour
            tow_vars = pd.get_dummies(tow, prefix="tow")
            out_init.loc[:, tow_vars.columns] = tow_vars
            return(out_init)

        else:
            raise ValueError(
                "Time interval supplied expected 'daily' or 'hourly'. "
                "Neither of those were given.")

    @staticmethod
    def get_tow(df, interval):
        """


        Parameters
        ----------
        df : TYPE
            DESCRIPTION.
        interval : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        df = df.copy()
        if interval.upper() == 'DAILY':
            df['tow'] = df['time'].dt.dayofweek

        elif interval.upper() == 'HOURLY':
            dow = df['time'].dt.dayofweek
            hour = df['time'].dt.hour
            df['tow'] = dow*24 + hour

        else:
            raise ValueError(
                "Time interval supplied expected 'daily' or 'hourly'. "
                "Neither of those were given.")

        df.drop(columns='time', inplace=True)
        return(df)
