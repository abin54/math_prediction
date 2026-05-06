import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, date
from prophet import Prophet
from prophet.serialize import model_from_json, model_to_json
import pandas as pd
import os

app = FastAPI(title="52-Year Daily Predictor")

# Load the model ONCE when the server starts
model = None
last_known_date = None

class PredictionResponse(BaseModel):
    date: str
    predicted_value: float
    lower_bound: float
    upper_bound: float

class UpdateRequest(BaseModel):
    date: str
    actual_value: float

@app.on_event("startup")
def load_model():
    global model, last_known_date
    print("Loading model...")
    try:
        with open('prophet_model.json', 'r') as f:
            model = model_from_json(f.read())
        
        # Figure out what the last date in the model is
        last_known_date = model.history['ds'].max()
        print(f"Model loaded. Last known date in history: {last_known_date}")
    except Exception as e:
        print(f"ERROR loading model: {e}")

@app.get("/predict/next7", response_model=list[PredictionResponse])
def predict_next_7_days():
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Create future dataframe starting from the day AFTER the last known date
    future = model.make_future_dataframe(periods=7, freq='D', include_history=False)
    
    forecast = model.predict(future)
    
    results = []
    for _, row in forecast.iterrows():
        results.append(PredictionResponse(
            date=row['ds'].strftime('%Y-%m-%d'),
            predicted_value=round(row['yhat'], 2),
            lower_bound=round(row['yhat_lower'], 2),
            upper_bound=round(row['yhat_upper'], 2)
        ))
    return results

@app.post("/update")
def update_model_with_actual_data(data: UpdateRequest):
    global model, last_known_date
    
    new_date = pd.to_datetime(data.date).normalize()
    new_row = pd.DataFrame({'ds': [new_date], 'y': [data.actual_value]})
    
    # Append the actual data to the model's history
    model.history = pd.concat([model.history, new_row]).sort_values('ds').reset_index(drop=True)
    
    # Optional: Save the updated model
    with open('prophet_model.json', 'w') as f:
        f.write(model_to_json(model))
        
    last_known_date = new_date
    return {"status": "success", "message": f"Model updated with {data.date}: {data.actual_value}"}

@app.get("/health")
def health():
    return {"status": "healthy", "last_known_date": str(last_known_date)}
