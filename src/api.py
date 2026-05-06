import pandas as pd
import os
import sys
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, Field

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import settings
from src.database import SessionLocal, get_db, get_historical_df, DailyValue
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
app = FastAPI(title="Enterprise Time Series Forecast")

# Global State Cache (Eliminates redundant DB I/O)
class StateCache:
    def __init__(self):
        self.df_hist: pd.DataFrame = pd.DataFrame()
        self.df_fe: pd.DataFrame = pd.DataFrame()
        self.models: dict = {}
        self.feature_cols: list = FeatureEngineer.get_feature_columns()

cache = StateCache()

@app.on_event("startup")
async def startup_event():
    logger.info("INIT", extra={"event": "startup"})
    
    # 1. Load Models & Validate Schema Binding
    for i in range(1, 8):
        path = f"models/xgb_day_{i}.json"
        if not os.path.exists(path):
            logger.error("MISSING_MODEL", extra={"model": path})
            continue
        m = xgb.XGBRegressor()
        m.load_model(path)
        
        # Validate Feature Schema Binding
        saved_features = m.get_booster().attr("feature_names")
        if saved_features:
            current_features = ",".join(cache.feature_cols)
            if saved_features != current_features:
                logger.critical("FEATURE_DRIFT_DETECTED", extra={"saved": saved_features, "current": current_features})
                raise RuntimeError(f"Feature drift in model {i}!")
                
        cache.models[i] = m
    
    # 2. Warm up the In-Memory Cache
    logger.info("WARMING_CACHE")
    cache.df_hist = await run_in_threadpool(get_historical_df, 1000)
    if not cache.df_hist.empty:
        cache.df_fe = await run_in_threadpool(FeatureEngineer.build_features, cache.df_hist)
        
    logger.info("STARTUP_COMPLETE", extra={"models": len(cache.models), "cache_rows": len(cache.df_fe)})

# --- STRICT PYDANTIC SCHEMAS ---
class ForecastItem(BaseModel):
    date: str
    predicted_value: float

class UpdateRequest(BaseModel):
    date: date
    value: float = Field(..., gt=-1e10, lt=1e10, description="Must be a valid number, not NaN or Inf")

# --- ENDPOINTS ---
@app.get("/forecast/next7", response_model=List[ForecastItem])
async def forecast_next_7_days():
    try:
        if len(cache.models) < 7:
            raise HTTPException(status_code=500, detail="Models not fully loaded.")
            
        if cache.df_fe.empty:
            logger.error("CACHE_EMPTY")
            raise HTTPException(status_code=400, detail="No historical data available in cache.")
            
        # Get the absolute latest row from in-memory cache (Zero I/O Latency)
        latest_row = cache.df_fe.iloc[-1:]
        X_latest = latest_row[cache.feature_cols]
        last_date = latest_row['ds'].values[0]
        
        predictions = []
        for i in range(1, 8):
            # Offload CPU-bound prediction to thread pool to prevent event loop blocking
            pred_val = await run_in_threadpool(cache.models[i].predict, X_latest)
            pred_date = pd.to_datetime(last_date) + pd.Timedelta(days=i)
            predictions.append(ForecastItem(
                date=pred_date.strftime('%Y-%m-%d'),
                predicted_value=round(float(pred_val[0]), 2)
            ))
            
        return predictions
        
    except Exception as e:
        logger.error("PREDICTION_FAILED", extra={"error": str(e)})
        raise HTTPException(status_code=500, detail="Internal prediction error")

def process_update(data: UpdateRequest):
    """Background task to sync cache and database without blocking the API."""
    db = SessionLocal()
    try:
        # 1. Update Database
        exists = db.query(DailyValue).filter(DailyValue.date == data.date).first()
        if exists:
            exists.value = data.value
        else:
            db.add(DailyValue(date=data.date, value=data.value))
        db.commit()
        
        # 2. Update In-Memory Cache
        new_row = pd.DataFrame({"ds": [data.date], "value": [data.value]})
        cache.df_hist = pd.concat([cache.df_hist, new_row]).drop_duplicates(subset='ds', keep='last').sort_values('ds')
        
        # Recalculate features for the tail (minimal CPU impact compared to full recalculation)
        cache.df_fe = FeatureEngineer.build_features(cache.df_hist)
        
        logger.info("CACHE_SYNC_COMPLETE", extra={"date": str(data.date)})
    finally:
        db.close()

@app.post("/update")
async def update_actual_value(data: UpdateRequest, background_tasks: BackgroundTasks):
    """Acknowledges data instantly; persistence and cache sync happen in the background."""
    background_tasks.add_task(process_update, data)
    return {"status": "accepted", "details": "Syncing with Sovereign Cache"}

@app.get("/health")
def health():
    return {"status": "healthy", "models_loaded": len(cache.models) == 7, "cache_size": len(cache.df_fe)}
