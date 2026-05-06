from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd
import src.model as model_module
import os
from src.database import init_db, SessionLocal, DailyRecord
from sqlalchemy.orm import Session
from fastapi import Depends

app = FastAPI(title="52-Year Daily Forecasting API")
predictor = model_module.DailyPredictor()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Load model and init DB on startup
@app.on_event("startup")
def startup_event():
    init_db()
    model_path = "models/latest_model.json"
    if os.path.exists(model_path):
        try:
            predictor.load_model(model_path)
            print("Production model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
    else:
        print("WARNING: Model not found! API will require training/loading before inference.")

class ForecastItem(BaseModel):
    date: str
    predicted_value: float

class UpdateRequest(BaseModel):
    date: str
    actual_value: float

@app.get("/forecast/next7", response_model=List[ForecastItem])
def get_7_day_forecast():
    """Returns the forecasted numbers for the next 7 days."""
    # In production, fetch last 400 days from DB
    # For now, we use the cleaned sandbox data as a source
    data_path = "daily_predictor/data.csv"
    if not os.path.exists(data_path):
        raise HTTPException(status_code=500, detail="Historical data source not found.")
        
    historical_df = pd.read_csv(data_path)
    historical_df.columns = ['ds', 'value']
    
    try:
        preds = predictor.predict_next_n(historical_df, 7)
        return preds
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update")
def update_actual_value(data: UpdateRequest, db: Session = Depends(get_db)):
    """Feeds today's actual number back into the system to keep the model fresh."""
    new_date = pd.to_datetime(data.date).date()
    
    # Check if record exists
    record = db.query(DailyRecord).filter(DailyRecord.date == new_date).first()
    if record:
        record.actual_value = data.actual_value
    else:
        record = DailyRecord(date=new_date, actual_value=data.actual_value)
        db.add(record)
    
    db.commit()
    return {"status": "success", "message": f"Recorded {data.actual_value} for {data.date}"}

@app.get("/health")
def health():
    model_loaded = hasattr(predictor.model, "feature_names_in_")
    return {"status": "healthy", "model_loaded": model_loaded}
