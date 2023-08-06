import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import warnings


class Model:
    """The parent NMEC model class that handles the shared methods between all
        the child classes as well as handles the data processing to create
        models on."""

    def __init__(self, df=None, dependent_col="load", temperature_col="temp",
                 dependent_df=None, temperature_df=None, occupancy_col=None,
                 additional_vars_df=None, model_name="TOWT"):
        """
        Initialize object by ensuring dataframe is fit for modeling and noting
        model specs.
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
        model_name : str, optional
            Specific model name, which will be used in child subclasses.
            TOWT options are: TOWT, TOWT
            ChangePoint options are: SLR, 3PC, 3PH, 4P, 5P
            HDD_CDD options are: HD, CD, HD-CD
            default is towt.

        Raises
        ------
        KeyError
            DESCRIPTION.
        ValueError
            DESCRIPTION.
        Returns
        -------
        None.
        """
        if model_name is not None:
            self.model_name = model_name.upper()
        else:
            self.model_name = model_name

        self.interval_tiers = {'Monthly': 1, 'Daily': 2,
                               'Hourly': 3, '15 Minute': 4}
        self.model_interval = None

        if df is not None:
            if isinstance(df, pd.DataFrame):
                self.df = df.copy()  # copy to not overwrite original df obj
                self.timestamp_col = self.__check_timestamp_col(df)
                self.min_interval = self.infer_interval(self.df,
                                                        self.timestamp_col)
                self.dependent_col = dependent_col
                self.temperature_col = temperature_col
                self.occupancy_col = occupancy_col
                not_x_cols = [self.timestamp_col,
                              self.dependent_col,
                              self.temperature_col,
                              self.occupancy_col]
                # x_train_cols does not include temp column because it can make
                # a variable number of extra columns depending on modeling algo
                self.x_train_cols = list(self.df.drop(
                    columns=[x for x in not_x_cols if x is not None]).columns)
                try:
                    self.df[[dependent_col]]
                except KeyError:
                    raise KeyError(
                        "Supplied dependent variable column name is " +
                        dependent_col + " but it was not found in the supplied"
                        " dataframe.")
            else:
                raise ValueError("Supplied dataset is not a pandas dataframe.")
            if dependent_df is not None:
                warnings.warn("df argument is assuming the full regression "
                              "dataset with the dependent variable and other "
                              "regressors. Another value was passed as the "
                              "dependent dataframe. Ignoring it.")

        elif dependent_df is not None:
            if isinstance(dependent_df, pd.DataFrame):
                self.temperature_col = None
                self.df = self.aggregate(dependent_df=dependent_df,
                                         temperature_df=temperature_df,
                                         additional_vars_df=additional_vars_df)
                self.occupancy_col = occupancy_col
                not_x_cols = [self.timestamp_col,
                              self.dependent_col,
                              self.temperature_col,
                              self.occupancy_col]
                self.x_train_cols = list(self.df.drop(
                    columns=[x for x in not_x_cols if x is not None]).columns)
                self.df.sort_values(by=self.timestamp_col)
            else:
                raise ValueError("Supplied dependent variable dataset is not a"
                                 "pandas DataFrame.")
        else:
            print("No data was provided for training.")
            self.df = None
            self.timestamp_col = None
            self.min_interval = None
            self.dependent_col = None
            self.temperature_col = None
            self.occupancy_col = None
            self.x_train_cols = None

        self.occ_model = None
        self.unocc_model = None

        if self.x_train_cols is not None:
            self.group_method = dict(
                zip([self.dependent_col, self.temperature_col,
                     self.occupancy_col] + self.x_train_cols,
                    ["sum", "mean", "max"] + ["sum" for x in
                                              range(len(self.x_train_cols))]))
            self.group_method.pop(None, None)
            
            # Get number of non-dependent columns
            self.train_col_list = self.x_train_cols.copy()
            self.train_col_list += [self.temperature_col]
            self.train_col_list += [self.occupancy_col] if self.occupancy_col is not None else []
        else:
            self.train_col_list = [self.temperature_col]
            self.train_col_list += [self.occupancy_col] if self.occupancy_col is not None else []
            

    def aggregate(self, dependent_df=None, temperature_df=None,
                  additional_vars_df=None):
        """
        Aggregate dataframes containing the different possible variables for
        regression.
        Parameters
        ----------
        dependent_df : Pandas DataFrame, optional
            Dataframe consisting of two columns: a timestamp column and the
            dependent variable column. The default is None.
        temperature_df : Pandas DataFrame, optional
            Dataframe consisting of two columns: a timestamp column and a
            temperature column. The default is None.
        additional_vars_df : Pandas DataFrame, optional
            Dataframe consisting of at least two columns: a timestamp column
            and any amount of other variables to be included in the regression.
            The default is None.
        Returns
        -------
        None.
        """

        max_time_col = self.__check_timestamp_col(dependent_df)
        min_interval = self.infer_interval(dependent_df,
                                           max_time_col)
        main_df = dependent_df.copy()
        self.dependent_col = (dependent_df.drop(
            columns=[max_time_col]).columns[0])
        if temperature_df is not None:
            temperature_df_time_col = self.__check_timestamp_col(
                temperature_df)
            self.temperature_col = (temperature_df.drop(
                columns=[temperature_df_time_col]).columns[0])
            temperature_df_interval = self.infer_interval(
                temperature_df, temperature_df_time_col)
            main_df = main_df.merge(temperature_df, how="outer",
                                    left_on=max_time_col,
                                    right_on=temperature_df_time_col)
            if self.interval_tiers[min_interval] > self.interval_tiers[temperature_df_interval]:
                min_interval = temperature_df_interval
                max_time_col = temperature_df_time_col

        if additional_vars_df is not None:
            additional_vars_df_time_col = self.__check_timestamp_col(
                additional_vars_df)
            additional_vars_df_interval = self.infer_interval(
                additional_vars_df, additional_vars_df_time_col)
            main_df = main_df.merge(additional_vars_df, how="outer",
                                    left_on=max_time_col,
                                    right_on=additional_vars_df_time_col)
            if self.interval_tiers[min_interval] > self.interval_tiers[additional_vars_df_interval]:
                min_interval = additional_vars_df_interval
                max_time_col = additional_vars_df_time_col

        self.min_interval = min_interval
        self.timestamp_col = max_time_col
        main_df.sort_values(by=max_time_col, inplace=True)
        main_df.reset_index(drop=True, inplace=True)
        return main_df

    @staticmethod
    def __check_timestamp_col(df):
        """
        Function to identify which column is the timestamp column in a
        dataframe.
        Parameters
        ----------
        df : Pandas DataFrame
            Dataframe with a datetime column.
        Raises
        ------
        TypeError
            No timestamp column could be found in the dataframe.
        Returns
        -------
        list
            List of size 1 containing a string name of the datetime column.
        """

        timestamp_cols = []
        for i in df.columns:
            if ((pd.core.dtypes.common.is_datetime_or_timedelta_dtype(df[i]))
                    | (pd.api.types.is_datetime64_ns_dtype(df[i]))):
                timestamp_cols.append(i)
        if len(timestamp_cols) == 0:
            raise TypeError(
                'Could not find any datetime/timestamp columns')
        elif len(timestamp_cols) == 1:
            return(timestamp_cols[0])
            return(timestamp_cols)
        elif len(timestamp_cols) > 1:
            print('Multiple timestamp/datetime columns were found. '
                  'Assuming the first one is for the dataset.')
            timestamp_cols = timestamp_cols[0]
            return(timestamp_cols)

    def train_test_split(self, df, train_ratio=0.5, train_dates=()):
        pass

    def find_occ_unocc(self, hd_base=50, cd_base=65, time_interval="Monthly",
                       occ_threshold=0.65, inplace=True):
        """
        Determine occupancy schedule based off usage.
        Parameters
        ----------
        df : Pandas DataFrame
            Pandas dataframe consisting of at a minimum a timestamp,
            temperature, and load column labelled time, temp, and load.
        occ_threshold : float, optional
            DESCRIPTION. The default is 0.65.
        Returns
        -------
        None.
        """

        if time_interval == "Monthly":
            self.df['occ'] = 1
            return(self.df)
        if occ_threshold == 1:
            self.df['occ'] = 1
            return(self.df)

        orig_copy = self.df.copy()

        self.df['t50'] = self.df[self.temperature_col] - hd_base
        self.df.loc[self.df['t50'] > 0, 't50'] = 0
        self.df['t65'] = self.df[self.temperature_col] - cd_base
        self.df.loc[self.df['t65'] < 0, 't65'] = 0
        df_regress = self.df[[self.timestamp_col,
                              self.dependent_col, 't50', 't65']].dropna()
        x_regress = df_regress.loc[:, ['t50', 't65']]
        y_regress = df_regress[self.dependent_col]
        occ_test_model = LinearRegression().fit(x_regress, y_regress)
        df_regress['predict'] = occ_test_model.predict(x_regress)
        df_regress['residual'] = df_regress[self.dependent_col] - \
            df_regress['predict']
        df_regress['residual_count'] = df_regress['residual'] > 0
        df_regress['count'] = 1

        if time_interval == "Daily":
            df_regress['tow'] = df_regress[self.timestamp_col].dt.dayofweek
        elif time_interval == "Hourly":
            df_regress['tow'] = df_regress[self.timestamp_col].dt.dayofweek * \
                24 + df_regress[self.timestamp_col].dt.hour

        threshold_count = df_regress[
            ['tow', 'residual_count',
             'count']].groupby('tow').sum().reset_index()
        threshold_count['occ'] = (threshold_count['residual_count'] /
                                  threshold_count['count'] >
                                  occ_threshold).replace({True: 1, False: 0})
        df_regress = df_regress.merge(
            threshold_count[['tow', 'occ']], on="tow", how="outer")
        self.df_regress = df_regress
        self.orig_copy = orig_copy
        out = orig_copy.merge(
            df_regress[[self.timestamp_col, 'occ']], on=self.timestamp_col,
            how='outer').sort_values(by=self.timestamp_col)
        if inplace:
            self.df = out
        else:
            self.df = orig_copy
            
        # Summarize occupancy schedule
        occ_sched = pd.DataFrame()
        if time_interval.upper()=="DAILY":
            tow = out[self.timestamp_col].dt.dayofweek
        elif time_interval.upper()=="HOURLY":
            dow = out[self.timestamp_col].dt.dayofweek
            hour = out[self.timestamp_col].dt.hour
            tow = dow*24+hour
        occ_sched['tow'] = tow
        occ_sched['occ'] = out['occ']
        occ_sched = occ_sched.groupby('tow').mean().to_dict()['occ']
        self.determined_occ_sched = occ_sched
        
        return(out)

    def format_results(self, prediction_df):
        """
        Parameters
        ----------
        prediction_df : TYPE
            DESCRIPTION.
        Returns
        -------
        None.
        """
        pass

    def train(self):
        pass

    def predict(self):
        pass

    @staticmethod
    def infer_interval(df, time_colname='time'):
        """
        Infers the time series interval in a supplied pandas dataframe.
        Parameters
        ----------
        df : pandas DataFrame
            Pandas DataFrame with at a minimum a timestamp column.
        time_colname : str or list of size 1 containing a str
            Value that provides what the timestamp column name is. The default
            is ['time'].
        Returns
        -------
        String that is Hourly, Daily, or Monthly.
        """

        # Get median number of minutes between observations
        minute_interval = df[time_colname].diff().apply(
            lambda x: x/np.timedelta64(1,
                                       'm')).fillna(0).astype('int64').median()

        if (minute_interval > 60/2) & (minute_interval < 60*2):
            time_interval = "Hourly"
            return(time_interval)
        elif(minute_interval > 10) & (minute_interval < 20):
            time_interval = "15 Minute"
            return(time_interval)
        elif (minute_interval > 1440/2) & (minute_interval < 1440*2):
            time_interval = "Daily"
            return(time_interval)
        elif (minute_interval > 40320/2) & (minute_interval < 40320*1.5):
            time_interval = "Monthly"
            return(time_interval)
        else:
            raise ValueError(
                "Could not infer time interval based off 'time' column in"
                " dataframe.")

    def group_interval(self, df=None, time_interval=None, group_method=None,
                       time_col="time"):
        """
        Parameters
        ----------
        df : TYPE, optional
            DESCRIPTION. The default is None.
        time_interval : TYPE, optional
            DESCRIPTION. The default is None.
        group_method : TYPE, optional
            DESCRIPTION. The default is None.
        time_col : TYPE, optional
            DESCRIPTION. The default is "time".
        Raises
        ------
        ValueError
            DESCRIPTION.
        Returns
        -------
        None.
        """

        # Checks
        if df is None:
            if self.df is not None:
                df = self.df.copy()
            else:
                raise ValueError("No dataframe was provided.")
        if time_interval is None:
            if self.min_interval is not None:
                time_interval = self.min_interval
            else:
                raise ValueError("No time interval was provided.")
        if group_method is None:
            if self.group_method is not None:
                group_method = self.group_method
            else:
                raise ValueError("No grouping method was provided for"
                                 " variables.")
        df['year'] = df[time_col].dt.year
        df['month'] = df[time_col].dt.month
        df['day'] = df[time_col].dt.day
        df['hour'] = df[time_col].dt.hour

        if time_interval == 'Hourly':
            temp_time_cols = ['year', 'month', 'day', 'hour']
        elif time_interval == 'Daily':
            temp_time_cols = ['year', 'month', 'day']
        elif time_interval == 'Monthly':
            temp_time_cols = ['year', 'month']

        main = df.groupby(temp_time_cols).agg(group_method).reset_index()
        main[time_col] = pd.to_datetime(main[temp_time_cols])
        main.drop(columns=temp_time_cols, inplace=True)

        return(main)


    def r2(self, df):
        rss = ((df['load'] - df['y_fit']) ** 2).sum()
        y_bar = df['load'].mean()
        tss = ((df['load'] - y_bar) ** 2).sum()
        r2 = 1 - (rss / tss)

        return np.round(r2, 4)

    def adj_r2(self, df):
        r_squared = self.r2(df)
        rt = ((1 - r_squared) * (len(df) - 1)) / \
            (len(df) - len(self.train_col_list) - 1)  # right term
        adj_r_squared = 1 - rt

        return np.round(adj_r_squared, 4)

    def cvrmse(self, df):
        """
        Coefficient of Variation of the Root Mean Square Error (Percentage)
        :param df:  pandas dataframe consisting of the data the model was built
                    off of with the predicted values
        """
        rmse = (((df['load'] - df['y_fit']) ** 2).sum() /
                (len(df) - len(self.train_col_list))) ** (1 / 2)
        cvrmse = rmse / df['load'].mean()

        return np.round(cvrmse, 4)

    def nmbe(self, df):
        nmbe = (df['load'] - df['y_fit']).sum() / df['load'].sum()

        return np.round(nmbe, 4)

    def metrics(self, df):
        
        return {'R2': self.r2(df),
                'adj R2': self.adj_r2(df),
                'CVRMSE': self.cvrmse(df),
                'NMBE': self.nmbe(df)}

