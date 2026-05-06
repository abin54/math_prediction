from prophet import Prophet
import pandas as pd
import os

# Load the prepared data
df = pd.read_csv('data/processed/prophet_data.csv')
df.columns = ['ds', 'y'] 
df['ds'] = pd.to_datetime(df['ds'])

print("--- [PROPHET TRAINING] ---")
# Initialize with multi-seasonality
model = Prophet(
    growth='linear',
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    changepoint_prior_scale=0.05
)

# Fit the model
model.fit(df)

# Predict the next 30 days
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Show today's prediction
today = pd.Timestamp.now().normalize()
today_forecast = forecast[forecast['ds'] >= today].head(1)

if not today_forecast.empty:
    pred_val = today_forecast['yhat'].values[0]
    print(f"Prophet Prediction for {today.strftime('%Y-%m-%d')}: {pred_val:.2f} (Digit: {int(round(pred_val)) % 10})")

# Save forecast
os.makedirs("models/forecasts", exist_ok=True)
forecast.to_csv("models/forecasts/prophet_forecast.csv", index=False)
print("Prophet Forecast saved to models/forecasts/prophet_forecast.csv")
