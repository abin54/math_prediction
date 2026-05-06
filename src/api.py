import logging
import json
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List
from datetime import date
import xgboost as xgb
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import settings
from src.database import get_db, get_historical_df, DailyValue
from src.features import FeatureEngineer

# --- STRUCTURED LOGGING ---
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_obj = {"level": record.levelname, "message": record.getMessage()}
        if hasattr(record, "extra"): log_obj.update(record.extra)
        return json.dumps(log_obj)

logger = logging.getLogger("api")
logger.setLevel(settings.log_level)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)

# --- APP SETUP ---
app = FastAPI(title="Production Time Series Forecast")

models = {}
feature_cols = FeatureEngineer.get_feature_columns()

@app.on_event("startup")
def load_models():
    logger.info("INIT", extra={"event": "startup"})
    for i in range(1, 8):
        path = f"models/xgb_day_{i}.json"
        if not os.path.exists(path):
            logger.error("MISSING_MODEL", extra={"model": path})
            # For local dev, don't crash if models aren't trained yet
            print(f"WARNING: Missing model file: {path}")
            continue
        m = xgb.XGBRegressor()
        m.load_model(path)
        models[i] = m
    logger.info("MODELS_LOADED", extra={"count": len(models)})

# --- STRICT PYDANTIC SCHEMAS ---
class ForecastItem(BaseModel):
    date: str
    predicted_value: float

class UpdateRequest(BaseModel):
    date: date
    value: float = Field(..., gt=-1e10, lt=1e10, description="Must be a valid number, not NaN or Inf")

# --- ENDPOINTS ---
@app.get("/forecast/next7", response_model=List[ForecastItem])
def forecast_next_7_days():
    try:
        if len(models) < 7:
            raise HTTPException(status_code=500, detail="Models not fully loaded. Run training first.")
            
        df_hist = get_historical_df(days=1000)
        if df_hist.empty:
            logger.error("EMPTY_DB")
            raise HTTPException(status_code=400, detail="Database empty.")
            
        df_fe = FeatureEngineer.build_features(df_hist)
        if df_fe.empty:
            raise HTTPException(status_code=400, detail="Insufficient data for 365-day lags.")
            
        X_latest = df_fe.iloc[-1:][feature_cols]
        predictions = []
        last_date = df_fe.iloc[-1]['ds']
        
        for i in range(1, 8):
            pred_val = models[i].predict(X_latest)[0]
            pred_date = pd.to_datetime(last_date) + pd.Timedelta(days=i)
            predictions.append(ForecastItem(
                date=pred_date.strftime('%Y-%m-%d'),
                predicted_value=round(float(pred_val), 2)
            ))
            
        logger.info("PREDICTION_MADE", extra={"target_days": 7})
        return predictions
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("PREDICTION_FAILED", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Internal prediction error")

@app.post("/update")
def update_actual_value(data: UpdateRequest, db=Depends(get_db)):
    exists = db.query(DailyValue).filter(DailyValue.date == data.date).first()
    if exists:
        exists.value = data.value
    else:
        db.add(DailyValue(date=data.date, value=data.value))
    db.commit()
    logger.info("DATA_UPDATED", extra={"date": str(data.date), "value": data.value})
    return {"status": "success"}

@app.get("/health")
def health():
    return {"status": "healthy", "models_loaded": len(models) == 7}
