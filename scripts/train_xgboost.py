import numpy as np
import pandas as pd
import xgboost as xgb
import os

def add_time_series_features(df):
    df['lag_1'] = df['y'].shift(1)
    df['lag_7'] = df['y'].shift(7)
    df['lag_30'] = df['y'].shift(30)
    df['lag_365'] = df['y'].shift(365)
    
    # Sine/Cosine for day of year
    df['day_of_year'] = df['ds'].dt.dayofyear
    df['sin_day'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
    df['cos_day'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
    
    return df.dropna()

# Load data
df = pd.read_csv('data/processed/prophet_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

print("--- [XGBOOST TRAINING] ---")
# Train ONLY on the last 5 years (1825 days) to avoid drift
df_recent = df.tail(1825).copy()
df_featured = add_time_series_features(df_recent)

X = df_featured.drop(['ds', 'y'], axis=1)
y = df_featured['y']

# Simple XGBoost Regressor
model = xgb.XGBRegressor(objective='reg:squarederror', n_estimators=1000)
model.fit(X, y)

# Predict for today
last_row = X.tail(1)
prediction = model.predict(last_row)
final_val = float(prediction[0])
print(f"XGBoost Prediction for Tomorrow: {final_val:.2f}")

# Save model and result
os.makedirs("models/xgboost", exist_ok=True)
model.save_model("models/xgboost/sovereign_xgb.json")

os.makedirs("models/forecasts", exist_ok=True)
with open("models/forecasts/xgboost_prediction.json", "w") as f:
    import json
    json.dump({"prediction": final_val, "digit": int(round(final_val)) % 10}, f)

print("XGBoost model and results saved.")
