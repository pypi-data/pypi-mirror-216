import os
import numpy as np
import pandas as pd
import seaborn as sns
from .ChangePointModel import ChangePointModel

class NMEC:
    """
    An implementation of peer-reviewed energy data analysis algorithms in Python for site-specific M&V.

    data_path: Str, optional Path to a file containing all data. The default is None.
    data_intervals: List, optional List of the intervals you want to create. If nothing is passed then possible intervals will be inferred. The default is [].
    eload_path: Str, optional Path to a file containing eload data. The default is None.
    temp_path: Str, optional Path to a file containing temp data. The default is None.
    additional_path: Str, optional Path to a file containing additional data. The default is None.
    """
    df = None

    def __init__(self, data_path=None, data_intervals=None, eload_path=None, 
                 temp_path=None, additional_path=None):
        if data_intervals is None:
            data_intervals = []
        self.data_path = data_path
        self.eload_path = eload_path
        self.temp_path = temp_path
        self.additional_path = additional_path
        self.data_intervals = data_intervals

    def load_data(self, path=""):
        """
        Loads data given the data paths


        Parameters
        ----------
        path : Str
            Data path that you want to load from. The default is "".

        Returns
        -------
        df: An unformatted dataframe, list, dict, or array
        """
        pass

    def format_df(self):
        """
        Formats the data for usage in Models
        Returns
        -------
        df: A formatted pandas df
        """
        pass

    def model_with_changepoint(self, df: pd, cp_type="SLR"):
        my_model = ChangePointModel(df, model_name=cp_type)
        
        if cp_type.upper() in ["3PH", "3PC"]:
            df = my_model.df
            train_estimate = my_model.train(df.dropna().copy())

            return {"occupied model": my_model.p, "unoccupied model": None,
                    "data": train_estimate
                    # 'metrics': my_model.metrics(train_estimate)
                    }

        elif cp_type.upper() in ["SLR", "2P"]:
            
            if 'occ' in my_model.df.columns:
                df_occ = my_model.df.loc[df['occ'] == 1]
                df_unocc = my_model.df.loc[df['occ'] == 0]
            else:
                df_occ = my_model.df
                df_unocc = None
                
            train_estimate = my_model.train_SLR(df_occ.dropna().copy())
            
            if df_unocc is not None:
                train_estimate = my_model.train_SLR(
                    df_unocc.dropna().copy(), train_estimate)

            if train_estimate is not None:
                return {"occupied model": my_model.lm, "unoccupied model": my_model.lm_unocc,
                        "data": train_estimate
                        # 'metrics': my_model.metrics(train_estimate)
                        }
            else:
                raise ValueError(
                    'No Training Estimate, check if Type is SLR, 2P, 3PH, or 3PC')
  

    def example(self, model_type=None):
        print("modeling with type", model_type)

        df = pd.read_csv(
            f'{os.getcwd()}/tests/data/example.csv', parse_dates=[1])

        # Clean up Load
        df['load'] = df['load'].astype(float)

        # Clean up time
        df['time'] = pd.to_datetime(df['time'], errors='coerce', utc=True)
        df['time'] = df['time'].dt.tz_convert('Etc/GMT+7')

        # Print results
        result = self.model_with_changepoint(df, cp_type = model_type)
        
        return result
    
    def plot_results(self, df):

        df_long = pd.melt(df, id_vars=['time', 'temp', 'occ'], value_name="eload", var_name="Measurement")
        df_long = df_long.replace({'load': 'Actual', 'predict': 'Prediction'}) 
        # df_long['occ'] = train_long['occ'].replace({0: 'Unoccupied', 1: 'Occupied'})    

        sns_plot = sns.relplot(data=df_long, x='temp', y='eload', hue="Measurement", s=40, linewidth=0)
        return sns_plot
