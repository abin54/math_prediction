import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os

def analyze_prophet_cycles(csv_path: str):
    """
    Trains Prophet on the full 52-year dataset and extracts seasonal components.
    """
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    df['y'] = pd.to_numeric(df['Open'], errors='coerce')
    df = df.dropna(subset=['Date', 'y']).sort_values('Date')
    
    prophet_df = df[['Date', 'y']].rename(columns={'Date': 'ds'})
    
    print(f"--- Training Prophet on {len(prophet_df)} nodes ---")
    model = Prophet(
        growth='linear',
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.05
    )
    
    model.fit(prophet_df)
    
    # Predict next 30 days
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    
    # Analyze components
    print("\n--- [PROPHET COMPONENT ANALYSIS] ---")
    
    # Since we can't easily 'see' the plot here, we'll extract the component values
    # Yearly seasonality
    yearly = forecast[['ds', 'yearly']].tail(365)
    peak_month = yearly.loc[yearly['yearly'].idxmax()]['ds'].month_name()
    low_month = yearly.loc[yearly['yearly'].idxmin()]['ds'].month_name()
    
    # Weekly seasonality
    # Prophet stores weekly components. We'll look at the last 7 days of the forecast
    weekly = forecast[['ds', 'weekly']].tail(30)
    # Group by day of week to find the average contribution
    weekly['dow'] = weekly['ds'].dt.day_name()
    dow_stats = weekly.groupby('dow')['weekly'].mean().sort_values(ascending=False)
    
    print(f"Peak Year Signal: {peak_month}")
    print(f"Low Year Signal: {low_month}")
    print("\nWeekly Signal Strength (Highest to Lowest):")
    print(dow_stats)
    
    # Save the full forecast
    os.makedirs("models/forecasts", exist_ok=True)
    forecast.to_csv("models/forecasts/prophet_30day_horizon.csv", index=False)
    
    print(f"\n30-Day Forecast saved. First 7 days horizon:")
    print(forecast[['ds', 'yhat']].tail(30).head(7))

if __name__ == "__main__":
    analyze_prophet_cycles("data/constitutional_master_v52.csv")
