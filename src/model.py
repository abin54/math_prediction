import xgboost as xgb
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from src.features import TimeSeriesFeatureEngineer
import os

class DailyPredictor:
    def __init__(self):
        self.model = xgb.XGBRegressor(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.8,
            objective='reg:absoluteerror', # Optimizes for MAE directly
            random_state=42
        )
        self.feature_engineer = TimeSeriesFeatureEngineer()
        self.feature_cols = [] # Will be set during training

    def train(self, df: pd.DataFrame) -> dict:
        df_fe = self.feature_engineer.create_features(df)
        
        # Chronological split: Train on all but last 365 days, test on last 365 days
        train = df_fe.iloc[:-365]
        test = df_fe.iloc[-365:]
        
        # Define feature columns (exclude 'ds' and target 'value')
        self.feature_cols = [c for c in df_fe.columns if c not in ['ds', 'value']]
        
        X_train, y_train = train[self.feature_cols], train['value']
        X_test, y_test = test[self.feature_cols], test['value']
        
        self.model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
        
        # Calculate real-world metrics
        preds = self.model.predict(X_test)
        metrics = {
            "MAE": mean_absolute_error(y_test, preds),
            "MAPE": mean_absolute_percentage_error(y_test, preds)
        }
        
        os.makedirs("models", exist_ok=True)
        self.save_model("models/latest_model.json")
        return metrics

    def predict_next_n(self, historical_df: pd.DataFrame, n_days: int) -> list:
        """Predicts N days into the future iteratively."""
        # Load model if not in memory
        if not hasattr(self.model, "feature_names_in_"):
            self.load_model("models/latest_model.json")
        
        predictions = []
        df_temp = historical_df.copy()
        
        # We need to predict day by day because day N+1 needs the lag from day N
        for _ in range(n_days):
            # 1. Engineer features for the current context
            df_fe = self.feature_engineer.create_features(df_temp)
            
            # 2. Extract features for the very next day
            # (In this recursive pattern, we assume the latest row of df_fe has what we need)
            latest_row = df_fe.tail(1)
            X_tomorrow = latest_row[self.feature_cols]
            
            # 3. Predict
            pred = self.model.predict(X_tomorrow)[0]
            
            # 4. Append to historical tracking for next iteration's lags
            tomorrow_date = latest_row['ds'].values[0] + pd.Timedelta(days=1)
            predictions.append({"date": tomorrow_date.strftime('%Y-%m-%d'), "predicted_value": float(pred)})
            
            new_row = pd.DataFrame({'ds': [tomorrow_date], 'value': [pred]})
            df_temp = pd.concat([df_temp, new_row], ignore_index=True)
            
        return predictions

    def save_model(self, path: str):
        self.model.save_model(path)

    def load_model(self, path: str):
        self.model.load_model(path)
        # Re-set feature columns after loading
        self.feature_cols = [f for f in self.model.feature_names_in_]
