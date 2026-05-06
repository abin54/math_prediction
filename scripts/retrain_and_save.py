import pandas as pd
from src.model import DailyPredictor
from src.database import SessionLocal, DailyRecord
import os

def retrain():
    # 1. Load baseline data
    data_path = "daily_predictor/data.csv"
    if not os.path.exists(data_path):
        print("Historical data not found.")
        return
        
    df_base = pd.read_csv(data_path)
    df_base.columns = ['ds', 'value']
    df_base['ds'] = pd.to_datetime(df_base['ds'])
    
    # 2. Merge with SQLite updates (if any)
    if os.path.exists("predictions.db"):
        db = SessionLocal()
        records = db.query(DailyRecord).filter(DailyRecord.actual_value != None).all()
        if records:
            df_updates = pd.DataFrame([
                {'ds': pd.to_datetime(r.date), 'value': r.actual_value} 
                for r in records
            ])
            df_combined = pd.concat([df_base, df_updates]).drop_duplicates(subset='ds', keep='last')
            df_combined = df_combined.sort_values('ds')
            print(f"Merged {len(df_updates)} updates from database.")
        else:
            df_combined = df_base
        db.close()
    else:
        df_combined = df_base
        
    # 3. Train
    predictor = DailyPredictor()
    print(f"Retraining on {len(df_combined)} rows...")
    metrics = predictor.train(df_combined)
    print(f"Retraining Complete. MAE: {metrics['MAE']:.4f}")

if __name__ == "__main__":
    retrain()
