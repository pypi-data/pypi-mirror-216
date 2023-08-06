import numpy as np
import pandas as pd
from scipy import optimize, stats
from .Model import Model


class ChangePointModel(Model):

    def __init__(self, df=None, dependent_col="load", temperature_col="temp",
                 dependent_df=None, temperature_df=None,
                 additional_vars_df=None, model_name="3PH"):
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
        model_name : str, optional
            Specific model name.
            Options are: SLR, 3PC, 3PH, 4P, 5P.
            Upper or lower case is accepted. Default is 3PH.

        Raises
        ------
        ValueError
            If specifed changepoint type is not recognized or not provided
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
                         model_name=model_name)

        if self.model_name not in ["SLR", "3PH", "3PC", "4P", "5P"]:
            raise ValueError("Unknonwn model type: " + self.model_name + ". "
                             "Please specify model_name as"
                             " 'SLR', '3PH', or '3PC', '4P' or '5P'.")
        self.model_fit = False


    def get_bounds(self, temperature):
        """
        Get temperature bounds for piecewise linear parameters

        Parameters
        ----------
        temperature : array, temperatures

        Returns
        -------
        bounds: dictinary of values

        """
        hcp_bound_percentile = 1
        ccp_bound_percentile = 99
        
        percentiles = hcp_bound_percentile, ccp_bound_percentile
        # heating change point, cooling change point limits
        lower_bound, upper_bound = np.percentile(temperature, percentiles)

        hcp_min = lower_bound  # Heating change-point minimum
        hcp_max = upper_bound  # Heating change-point maximum
        ccp_min = lower_bound  # Cooling change-point minimum
        ccp_max = upper_bound  # Cooling change-point minimum
        base_min = 0  # Baseload minimum
        base_max = np.inf  # Baseload maximum
        hsl_min = -np.inf  # Heating slope minimum
        hsl_max = 0  # Heating slope maximum
        csl_min = 0  # Cooling slope minimum
        csl_max = np.inf  # Cooling slope maximum
        
        if self.model_name == "SLR":
            hsl_max = np.inf
        
        if self.model_name == "5P":
            midpoint = np.percentile(temperature, 50)
            hcp_max = midpoint
            ccp_min = midpoint
            
        # if self.model_name == "4P":
        #     csl_min = -np.inf
        #     hsl_max = np.inf
            
        
        training_bounds = ([hcp_min, ccp_min, base_min, hsl_min, csl_min],
                           [hcp_max, ccp_max, base_max, hsl_max, csl_max])
            
        return training_bounds
    
    
    def piecewise_linear(self, x, hcp, ccp, base, hsl, csl):
        #  hsl  \              / csl
        #        \            /
        #  base   \__________/
        #        hcp        ccp
    
    
        if self.model_name == "SLR":
            conds = [x]
            funcs = [lambda x: hsl * x + base]
            self.coeff_validation = {'hcp': False, 'ccp': False, 'base': True, 'hsl':True, 'csl': False}
        
        if self.model_name == "3PH":
            conds = [x > ccp, x <= ccp]
            funcs = [lambda x: base, 
                     lambda x: hsl * x + base - hsl * ccp]
            self.coeff_validation = {'hcp': True, 'ccp': False, 'base': True, 'hsl': True, 'csl': False}
            
        if self.model_name == "3PC":
            conds = [x < ccp, x >= ccp]
            funcs = [lambda x: base,
                     lambda x: csl * x + base - csl * ccp]

            self.coeff_validation = {'hcp': False, 'ccp': True, 'base': True, 'hsl': False, 'csl': True}
            
        if self.model_name == "4P":
            conds = [x < ccp, x >= ccp]
        
            funcs = [lambda x: hsl * x + base - hsl * ccp,
                     lambda x: csl * x + base - csl * ccp]
            
            ccp = hcp
            self.coeff_validation = {'hcp': True, 'ccp': False, 'base': True, 'hsl': True, 'csl': True}
        
        if self.model_name == "5P":
            
            conds = [x < hcp, (x >= hcp) & (x < ccp), x >= ccp]
        
            funcs = [lambda x: hsl * x + base - hsl * hcp,
                     lambda x: base,
                     lambda x: csl * x + base - csl * ccp]
            self.coeff_validation = {'hcp': True, 'ccp': True, 'base': True, 'hsl': True, 'csl': True}
    
        return np.piecewise(x, conds, funcs)
    
    
    
    def fit_model(self, x, y):
        """
        Fit a change point model to the data.

        Parameters
        ----------
        x : numpy array
            Temperature
        y : numpy array
            Load

        Returns
        -------
        y_fit : numpy array
            Fitted load values

        """
        x = np.array(x)
        y = np.array(y)

        model_bounds = self.get_bounds(temperature = x)
        
        p, e = optimize.curve_fit(f = self.piecewise_linear, 
                                  xdata = x, 
                                  ydata = y, 
                                  bounds = model_bounds)
                                  #p0 = [64, 0, 11408, -290, 0])
        y_fit = self.piecewise_linear(x, *p)
        return p, y_fit
    

    def train(self, interval=None):
        """
        Training method for change point models (SLR, 3PC, 3PH, 4P, 5P)

        Parameters
        ----------
        interval: str, optional
            Desired interval to aggregate data to for training. 
            If None is provided then the finest granulairty possible is used.

        Returns
        -------
        Pandas Dataframe 
            Origianl training data with fitted values added
        """
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
                ' is unavailable. Finest granularity interval is ' + 
                self.min_interval + '.')
        self.model_interval = interval
        
        train = self.df.dropna().copy()
        
        x_train = train[self.temperature_col]
        y_train = train[self.dependent_col]
        
        coeffs, y_fit = self.fit_model(x_train, y_train)
        
        coef_dict = {}
        for k, v in zip(self.coeff_validation.keys(), coeffs):
            if self.coeff_validation[k]:
                coef_dict[k] = v
        self.coef_ = coef_dict
        
        train_estimate = pd.DataFrame({'time': train[self.timestamp_col],
                                       'temp': train[self.temperature_col],
                                       'load': train[self.dependent_col],
                                       'y_fit': y_fit}) 
        self.model_fit = True
        return train_estimate


    def predict(self, df=None):
        
        if df is None:
            raise ValueError(
                'No prediction df specified. Please pass a df to predict on.')
        if not self.model_fit:
            raise ValueError(
                'No trained model. Please train a model.')
        
        # predict_ts_col = self.__check_timestamp_col(df)

        predict_interval = self.infer_interval(df)
        
        min_predict_interval_num = self.interval_tiers[predict_interval]
        model_interval_num = self.interval_tiers[self.model_interval]

        if min_predict_interval_num > model_interval_num:
            df = self.group_interval(time_interval=self.model_interval,
                                          time_col=self.timestamp_col)
        
        if min_predict_interval_num < model_interval_num:
            raise ValueError(
                'Modeled interval: ' + self.model_interval + 
                ' does not match data interval: ' + predict_interval + '.')
        
        main = df.dropna().copy()
        x_pred = np.array(main[self.temperature_col])
        y_pred = self.piecewise_linear(x_pred, *self.coef_)
        
        predictions = pd.DataFrame({'time': main[self.timestamp_col],
                                   'temp': main[self.temperature_col],
                                   'predict': y_pred}) 
        
        return predictions
        
