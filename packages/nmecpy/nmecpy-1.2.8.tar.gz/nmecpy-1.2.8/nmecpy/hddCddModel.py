from Model import Model
import pandas as pd
from sklearn.linear_model import LinearRegression


class HDDCDDModel(Model):

    def __init__(self, df=None, dependent_col="load", temperature_col="temp",
                 occupancy_col=None, dependent_df=None, temperature_df=None,
                 additional_vars_df=None, HD_balancepoint=65,
                 CD_balancepoint=65, model_name='HD-CD'):
        """
        The class assumes a dataframe with HD and CD values that are already
        calculated.

        Parameters
        ----------
        df : Pandas DataFrame, optional
            If training a model, a dataframe must be provided. If using only
            for predictions, a dataframe is not needed when initialized.

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
        self.HD_balancepoint = HD_balancepoint
        self.CD_balancepoint = CD_balancepoint
        if df is not None:
            self.df['CD'] = self.df[self.temperature_col] - CD_balancepoint
            self.df.loc[self.df['CD'] < 0, 'CD'] = 0
            self.df['HD'] = HD_balancepoint - self.df[self.temperature_col]
            self.df.loc[self.df['HD'] < 0, 'HD'] = 0
        self.temp_train_cols = []
        self.group_method['CD'] = 'sum'
        self.group_method['HD'] = 'sum'
        self.model = None

    def train(self, model="HD-CD", interval=None):
        """
        Model training method for heating degree and cooling degree models.

        Parameters
        ----------
        model : str, optional
            String value equaling HD-CD for a heating and cooling degree model.
            HD for just a heating degree model. CD for just a cooling degree
            model. The default is "HD-CD".
        interval : str, optional
            String value to specify which interval the model should be ran at.
            If no value is given, it will default to the minimum possible
            interval.

        Returns
        -------
        out : Pandas DataFrame
            Modeled dataframe with predicted values.

        """

        # Checks
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

        if model == "HD-CD":
            self.temp_train_cols = ['HD', 'CD']
            self.x_train_cols = list(
                set(self.x_train_cols + self.temp_train_cols))
        elif model == "HD":
            self.temp_train_cols = ['HD']
            self.x_train_cols = list(
                set(self.x_train_cols + self.temp_train_cols))
        elif model == "CD":
            self.temp_train_cols = ['CD']
            self.x_train_cols = list(
                set(self.x_train_cols + self.temp_train_cols))
        else:
            raise ValueError(
                'No model name was provided. Provide either HD-CD, HD, or CD')

        # Assemble regression datasets
        # if ('occ' not in self.df.columns):
        #     self.df = self.find_occ_unocc(time_interval=time_interval)

        main = self.df.copy()
        train = main[[self.dependent_col, self.timestamp_col]
                     + self.x_train_cols].dropna().copy()
        x_train = train[self.x_train_cols]
        y_train = train[[self.dependent_col]]
        self.model = LinearRegression().fit(x_train, y_train)
        train['yhat'] = self.model.predict(x_train)
        out = train[[self.timestamp_col, 'yhat']].merge(
            main, on=self.timestamp_col, how='outer')

        print("Model completed running. Check model attribute.")

        return(out)

    def predict(self, df, timestamp_col='time'):
        """
        Predict method for heating degree and cooling degree methods.

        Parameters
        ----------
        df : Pandas DataFrame
            Dataframe with heating and/or cooling degree variables.
        occ_model : sklearn LinearRegression object, optional
            Regression object for occipied model. This is required. If None,
            will assume it is an object attribute.
        unocc_model : sklearn LinearRegression object, optional
            Regression object for unoccipied model. The default is None.
            If None, will assume it is an object attribute. If object attribute
            is also None, will assume there is no unoccupied model to predict
            on.

        Returns
        -------
        Predictions attached to main dataframe.

        """

        # Checks
        if self.model is None:
            raise ValueError("Create a model using train method.")

        check_cols = all(item in df.columns for item in
                         [self.dependent_col, timestamp_col]+self.x_train_cols)
        if not check_cols:
            raise ValueError("Missing either the dependent col, timestamp col,"
                             " or one of the explanatory variables.")

        temp_time_col = timestamp_col

        # Predict
        main = df.copy()
        pred = main[[self.dependent_col, timestamp_col] +
                    self.x_train_cols].dropna().copy()

        x_pred = pred[self.x_train_cols]
        pred['predict'] = self.model.predict(x_pred)
        out = pred[[temp_time_col, 'predict']].merge(
            main, on=temp_time_col, how='outer')
        return(out)
