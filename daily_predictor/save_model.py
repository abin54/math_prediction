import pandas as pd
from prophet import Prophet
import json
import os

# Move to the sandbox directory to ensure relative paths work
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("Loading 52-year dataset...")
df = pd.read_csv('data.csv')
df.columns = ['ds', 'y']
df['ds'] = pd.to_datetime(df['ds'])
df = df.dropna()

print(f"Training Prophet Model on {len(df)} nodes...")
model = Prophet(
    yearly_seasonality=True, 
    weekly_seasonality=True, 
    daily_seasonality=False
)
model.fit(df)

from prophet.serialize import model_to_json

# Prophet models are saved as JSON files
print("Serializing model brain to JSON...")
with open('prophet_model.json', 'w') as f:
    f.write(model_to_json(model))

print("SUCCESS: Model brain saved to prophet_model.json")
