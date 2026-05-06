import numpy as np
import pandas as pd
import xgboost as xgb
import os

def create_multistep_features(df, horizon=30):
    """
    Creates features for multi-step forecasting.
    Instead of predicting t+1, we shift the target to create a window.
    """
    df = df.copy()
    for i in range(1, horizon + 1):
        df[f'lag_{i}'] = df['y'].shift(i)
    
    # Yearly seasonality features
    df['day_of_year'] = df['ds'].dt.dayofyear
    df['sin_day'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
    df['cos_day'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
    
    return df.dropna()

def train_multistep_xgboost(csv_path: str, horizon=30):
    df = pd.read_csv(csv_path)
    df['ds'] = pd.to_datetime(df['ds'])
    
    print(f"--- Training Multi-Step XGBoost (Horizon: {horizon}) ---")
    
    # Train only on last 10 years to capture recent regime
    df_recent = df.tail(365 * 10).copy()
    df_featured = create_multistep_features(df_recent, horizon)
    
    X = df_featured.drop(['ds', 'y'], axis=1)
    y = df_featured['y']
    
    model = xgb.XGBRegressor(
        objective='reg:squarederror', 
        n_estimators=1000,
        learning_rate=0.01,
        max_depth=6
    )
    model.fit(X, y)
    
    # Multi-step recursive prediction
    last_window = df_recent['y'].tail(horizon).values.tolist()
    predictions = []
    
    current_date = df_recent['ds'].max()
    
    for i in range(horizon):
        # Prepare features for current step
        # Lags are the last 'horizon' values
        lags = list(reversed(last_window))
        
        day_val = (current_date + pd.Timedelta(days=i+1)).dayofyear
        sin_d = np.sin(2 * np.pi * day_val / 365)
        cos_d = np.cos(2 * np.pi * day_val / 365)
        
        feat_vec = lags + [day_val, sin_d, cos_d]
        
        pred = model.predict(np.array([feat_vec]))[0]
        predictions.append(pred)
        
        # Update window for next step
        last_window.append(pred)
        last_window.pop(0)
        
    print("\n--- [XGBOOST MULTI-STEP RESULTS] ---")
    for i, p in enumerate(predictions[:7]):
        date_str = (current_date + pd.Timedelta(days=i+1)).strftime('%Y-%m-%d')
        print(f"Day {i+1} ({date_str}): {p:.2f} (Digit: {int(round(p)) % 10})")
        
    # Save results
    os.makedirs("models/forecasts", exist_ok=True)
    pd.DataFrame({
        'ds': [current_date + pd.Timedelta(days=i+1) for i in range(horizon)],
        'yhat': predictions
    }).to_csv("models/forecasts/xgboost_30day_horizon.csv", index=False)
    print("\nMulti-step forecast saved to models/forecasts/xgboost_30day_horizon.csv")

if __name__ == "__main__":
    train_multistep_xgboost("data/processed/prophet_data.csv")
