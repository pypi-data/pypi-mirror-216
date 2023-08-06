from .Model import Model
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


class STOWTModel(Model):

    def __init__(self, df=None, dependent_col="load", temperature_col="temp",
                 occupancy_col=None, dependent_df=None, temperature_df=None,
                 additional_vars_df=None, occ_threshold=0.65,
                 knot_temps=[40, 55, 65, 80, 90], model_name="TOWT"):
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
        self.knot_temps = knot_temps

        if self.model_name not in ["TOWT", "TOW"]:
            raise ValueError("Unknown model type: " + self.model_name + ". "
                             "Please specify model_name as TOW or TOWT.")

    def train(self, interval=None, knot_temps=None,
              seasons={'summer': [6, 7, 8, 9], 'winter': [1, 2, 3, 12],
                       'shoulder': [4, 5, 10, 11]}):
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

        main = pd.concat([self.df, temp_vars, tow_vars], axis=1)
        train = main.dropna().copy()

        # Define season cols and train
        train['month'] = train[self.timestamp_col].dt.month
        train['season'] = ""
        mods = {}
        for i in seasons.keys():
            train.loc[train['month'].isin(seasons[i]), 'season'] = i
            temp = train.loc[train['season'] == i, :].copy()
            x_train = temp[self.x_train_cols].copy()
            x_train.drop(columns=self.tow_train_cols[-1], inplace=True)
            y_train = temp.loc[:, self.dependent_col].copy()
            temp_mod = LinearRegression().fit(x_train, y_train)
            mods[i] = temp_mod

        self.seasons = seasons
        self.models = mods
        return(mods)

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

        pred['month'] = pred[self.timestamp_col].dt.month
        pred['season'] = ""
        temp_out = pd.DataFrame()
        for i in self.seasons.keys():
            pred.loc[pred['month'].isin(self.seasons[i]), 'season'] = i
            x_pred = pred.loc[pred['season'] == i,
                              self.models[i].feature_names_in_].copy()
            temp_dates = pred.loc[pred['season']
                                  == i, [self.timestamp_col]].copy()
            temp_dates['predict'] = self.models[i].predict(x_pred)
            temp_out = pd.concat([temp_out, temp_dates], axis=0)

        main_out = df.merge(temp_out, on="time", how="inner")
        return(main_out)

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
