import pandas as pd
import numpy as np

class FeatureEngineer:
    @staticmethod
    def build_features(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['ds'] = pd.to_datetime(df['ds'])
        df['day_of_week'] = df['ds'].dt.dayofweek
        df['day_of_year'] = df['ds'].dt.dayofyear
        df['sin_dayofyear'] = np.sin(2 * np.pi * df['day_of_year']/365)
        df['cos_dayofyear'] = np.cos(2 * np.pi * df['day_of_year']/365)
        df['sin_week'] = np.sin(2 * np.pi * df['day_of_week']/7)
        df['cos_week'] = np.cos(2 * np.pi * df['day_of_week']/7)
        df['lag_1'] = df['value'].shift(1)
        df['lag_7'] = df['value'].shift(7)
        df['lag_30'] = df['value'].shift(30)
        df['lag_365'] = df['value'].shift(365)
        df['rolling_mean_7'] = df['value'].rolling(window=7).mean().shift(1)
        df['rolling_std_7'] = df['value'].rolling(window=7).std().shift(1)
        df['rolling_mean_30'] = df['value'].rolling(window=30).mean().shift(1)
        df['diff_1'] = df['value'].diff(1)
        df['diff_7'] = df['value'].diff(7)
        return df.dropna()

    @staticmethod
    def get_feature_columns() -> list[str]:
        return [
            'day_of_week', 'sin_dayofyear', 'cos_dayofyear', 'sin_week', 'cos_week',
            'lag_1', 'lag_7', 'lag_30', 'lag_365',
            'rolling_mean_7', 'rolling_std_7', 'rolling_mean_30',
            'diff_1', 'diff_7'
        ]
