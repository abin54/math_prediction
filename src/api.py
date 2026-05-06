from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from datetime import date
import xgboost as xgb
import pandas as pd
import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import get_db, get_historical_df, DailyValue
from src.features import FeatureEngineer

app = FastAPI(title="52-Year Time Series Forecast")

# Hold the 7 models in memory
models = {}
feature_engineer = FeatureEngineer()
feature_cols = feature_engineer.get_feature_columns()

@app.on_event("startup")
def load_models():
    print("Loading 7 forecasting models into memory...")
    for i in range(1, 8):
        path = f"models/xgb_day_{i}.json"
        if not os.path.exists(path):
            print(f"WARNING: Missing model file: {path}. Predictions will fail until trained.")
            continue
        m = xgb.XGBRegressor()
        m.load_model(path)
        models[i] = m
    print(f"{len(models)} models loaded successfully.")

class ForecastItem(BaseModel):
    date: str
    predicted_value: float

class UpdateRequest(BaseModel):
    date: date
    value: float

@app.get("/forecast/next7", response_model=List[ForecastItem])
def forecast_next_7_days():
    try:
        if len(models) < 7:
             raise HTTPException(status_code=500, detail="Models not fully loaded. Run training first.")
             
        df_hist = get_historical_df(days=800)
        print(f"DEBUG: df_hist shape: {df_hist.shape}")
        if df_hist.empty:
             raise HTTPException(status_code=500, detail="Database is empty. Please seed data first.")
             
        df_fe = feature_engineer.build_features(df_hist)
        print(f"DEBUG: df_fe shape: {df_fe.shape}")
        
        # 2. Get the absolute latest row (Yesterday/Today)
        latest_data = df_fe.iloc[-1:]
        X_latest = latest_data[feature_cols]
        
        # 3. Predict using all 7 models simultaneously
        predictions = []
        last_date = latest_data['ds'].values[0]
        
        for i in range(1, 8):
            pred_val = models[i].predict(X_latest)[0]
            # Convert numpy timestamp to pandas timestamp if needed
            pred_date = pd.to_datetime(last_date) + pd.Timedelta(days=i)
            
            predictions.append(ForecastItem(
                date=pred_date.strftime('%Y-%m-%d'),
                predicted_value=round(float(pred_val), 2)
            ))
            
        return predictions
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update")
def update_actual_value(data: UpdateRequest, db=Depends(get_db)):
    """Ingests today's actual value so the DB is ready for tomorrow's forecast."""
    exists = db.query(DailyValue).filter(DailyValue.date == data.date).first()
    if exists:
        exists.value = data.value # Update if exists
    else:
        db.add(DailyValue(date=data.date, value=data.value))
    db.commit()
    return {"status": "success", "message": f"Recorded {data.value} for {data.date}"}

@app.get("/health")
def health():
    return {"status": "healthy", "models_loaded": len(models) == 7}
