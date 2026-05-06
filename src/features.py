import pandas as pd
import numpy as np

class TimeSeriesFeatureEngineer:
    def __init__(self, target_col: str = 'value'):
        self.target_col = target_col

    def create_features(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df['ds'] = pd.to_datetime(df['ds'])
        
        # 1. Calendar Features
        df['day_of_week'] = df['ds'].dt.dayofweek
        df['day_of_year'] = df['ds'].dt.dayofyear
        df['month'] = df['ds'].dt.month
        df['year'] = df['ds'].dt.year
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # 2. Cyclical Encoding (Crucial so the model knows Dec 31 is next to Jan 1)
        df['sin_dayofyear'] = np.sin(2 * np.pi * df['day_of_year']/365)
        df['cos_dayofyear'] = np.cos(2 * np.pi * df['day_of_year']/365)
        df['sin_week'] = np.sin(2 * np.pi * df['day_of_week']/7)
        df['cos_week'] = np.cos(2 * np.pi * df['day_of_week']/7)
        
        # 3. Lag Features (What happened X days ago?)
        for lag in [1, 7, 14, 30, 365]:
            df[f'lag_{lag}'] = df[self.target_col].shift(lag)
            
        # 4. Rolling Window Features (Trends)
        df['rolling_mean_7'] = df[self.target_col].rolling(window=7).mean().shift(1)
        df['rolling_std_7'] = df[self.target_col].rolling(window=7).std().shift(1)
        df['rolling_mean_30'] = df[self.target_col].rolling(window=30).mean().shift(1)
        
        # 5. Difference Features (Momentum)
        df['diff_1'] = df[self.target_col].diff(1)
        df['diff_7'] = df[self.target_col].diff(7)
        
        return df.dropna()

    def get_latest_features(self, df: pd.DataFrame, prediction_date: pd.Timestamp) -> pd.DataFrame:
        """Generates features for a future date based on historical data."""
        # Note: In production, you'd fetch the last 365 days to calculate lags.
        # This implementation ensures that the recursive prediction has all necessary columns.
        df_fe = self.create_features(df)
        return df_fe.tail(1)
