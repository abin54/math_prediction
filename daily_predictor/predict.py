import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# 1. Load your 52 years of data
print("Loading data...")
df = pd.read_csv('data.csv')

# Ensure columns are named exactly 'ds' and 'y'
df.columns = ['ds', 'y']
df['ds'] = pd.to_datetime(df['ds'])

# Drop any rows where the number is missing
df = df.dropna()

print(f"Loaded {len(df)} days of data.")

# 2. Initialize the Model
print("Training model (this might take 30-60 seconds)...")
model = Prophet(
    yearly_seasonality=True,   # Captures the 365-day loop
    weekly_seasonality=True,   # Captures the Mon-Sun loop
    daily_seasonality=False,   # You don't need hourly
    changepoint_prior_scale=0.1 # Makes it sensitive to recent trends
)

# 3. Train it on all 52 years
model.fit(df)

# 4. Ask for the future
# Calculate days to reach Actual Tomorrow (May 7, 2026)
last_date = df['ds'].max()
actual_tomorrow = pd.Timestamp.now().normalize() + pd.Timedelta(days=1)
days_to_predict = (actual_tomorrow - last_date).days

print(f"Extending forecast by {days_to_predict} days to reach {actual_tomorrow.strftime('%Y-%m-%d')}...")

# Create a dataframe up to tomorrow
future_tomorrow = model.make_future_dataframe(periods=days_to_predict, freq='D')

# Predict tomorrow
forecast_tomorrow = model.predict(future_tomorrow)

# Extract tomorrow's prediction
tomorrow_row = forecast_tomorrow.iloc[-1]
predicted_number = tomorrow_row['yhat']
lower_bound = tomorrow_row['yhat_lower']
upper_bound = tomorrow_row['yhat_upper']

print("\n" + "="*40)
print(f"DATE: {tomorrow_row['ds'].strftime('%Y-%m-%d')}")
print(f"PREDICTION: {predicted_number:.2f}")
print(f"LOWER BOUND: {lower_bound:.2f}")
print(f"UPPER BOUND: {upper_bound:.2f}")
print("="*40 + "\n")

# 5. Save the prediction to a file
output = pd.DataFrame({
    'date': [tomorrow_row['ds']],
    'predicted_value': [predicted_number],
    'lower_bound': [lower_bound],
    'upper_bound': [upper_bound]
})
output.to_csv('tomorrows_prediction.csv', index=False)
print("Saved to 'tomorrows_prediction.csv'")

# 6. Generate the diagnostic plots (THIS IS THE MOST IMPORTANT PART)
print("Generating analysis plots...")
fig1 = model.plot_components(forecast_tomorrow)
plt.savefig('pattern_analysis.png', dpi=150, bbox_inches='tight')
print("Saved 'pattern_analysis.png'. OPEN THIS IMAGE AND LOOK AT IT.")
