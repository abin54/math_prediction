import pandas as pd
import numpy as np
import os
from datetime import datetime

class SovereignEnsemble:
    """
    Unifies predictions from Prophet, Chronos, NeuralForecast, and XGBoost.
    """
    def __init__(self, forecast_dir="models/forecasts"):
        self.forecast_dir = forecast_dir
        
    def get_consensus(self):
        predictions = {}
        
        # 1. Load Prophet
        p_path = os.path.join(self.forecast_dir, "prophet_forecast.csv")
        if os.path.exists(p_path):
            p_df = pd.read_csv(p_path)
            p_df['ds'] = pd.to_datetime(p_df['ds'])
            today = pd.Timestamp.now().normalize()
            p_today = p_df[p_df['ds'] >= today].head(1)
            if not p_today.empty:
                predictions['Prophet'] = int(round(p_today['yhat'].values[0])) % 10

        # 2. Load XGBoost
        x_path = os.path.join(self.forecast_dir, "xgboost_prediction.json")
        if os.path.exists(x_path):
            import json
            with open(x_path, "r") as f:
                x_data = json.load(f)
                predictions['XGBoost'] = x_data['digit']
        
        # 3. Load Chronos
        c_path = os.path.join(self.forecast_dir, "chronos_prediction.npy")
        if os.path.exists(c_path):
            c_pred = np.load(c_path)
            predictions['Chronos'] = int(round(c_pred[0][0])) % 10
            
        # 4. Load NeuralForecast
        n_path = os.path.join(self.forecast_dir, "neuralforecast_prediction.csv")
        if os.path.exists(n_path):
            n_df = pd.read_csv(n_path)
            predictions['NeuralForecast'] = int(round(n_df['NHITS'].values[0])) % 10
            
        return predictions

    def calculate_swarm_digit(self):
        preds = self.get_consensus()
        if not preds:
            return None
            
        vals = list(preds.values())
        print(f"  [Swarm] Collected Predictions: {preds}")
        
        # Simple Majority Vote
        counts = np.bincount(vals)
        majority_digit = np.argmax(counts)
        
        return majority_digit

if __name__ == "__main__":
    ensemble = SovereignEnsemble()
    digit = ensemble.calculate_swarm_digit()
    print(f"Final Swarm Consensus Digit: {digit}")
