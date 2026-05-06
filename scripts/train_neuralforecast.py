import pandas as pd
from neuralforecast import NeuralForecast
from neuralforecast.models import NHITS
import os

# Load the prepared data
df = pd.read_csv('data/processed/neuralforecast_data.csv')
df['ds'] = pd.to_datetime(df['ds'])

print("--- [NEURALFORECAST TRAINING] ---")
# N-HiTS configuration for daily data
model = NHITS(
    h=30,                  # Forecast horizon: predict next 30 days
    input_size=365 * 3,    # Look back 3 years
    max_steps=500,         # Reduced for faster demonstration
    n_freq_downsample=[1, 1, 1],
)

nf = NeuralForecast(models=[model], freq='D')
nf.fit(df)

# Predict
forecast_df = nf.predict()
print("NeuralForecast (NHITS) Prediction for Tomorrow:")
print(forecast_df.head(1))

# Save results
os.makedirs("models/forecasts", exist_ok=True)
forecast_df.to_csv("models/forecasts/neuralforecast_prediction.csv")
print("NeuralForecast results saved to models/forecasts/neuralforecast_prediction.csv")
