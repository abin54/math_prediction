import pandas as pd
import xgboost as xgb
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import SessionLocal, DailyValue
from src.features import FeatureEngineer

def ingest_csv(csv_path: str):
    print(f"Ingesting {csv_path}...")
    df = pd.read_csv(csv_path)
    df.columns = ['date', 'value'] 
    df['date'] = pd.to_datetime(df['date']).dt.date
    
    db = SessionLocal()
    count = 0
    for _, row in df.iterrows():
        exists = db.query(DailyValue).filter(DailyValue.date == row['date']).first()
        if not exists:
            db.add(DailyValue(date=row['date'], value=row['value']))
            count += 1
    db.commit()
    db.close()
    print(f"Added {count} records.")

def train_models():
    from src.database import get_historical_df
    df = get_historical_df(days=20000)
    if df.empty:
        print("ERROR: No data in DB to train on.")
        return
        
    df_fe = FeatureEngineer.build_features(df)
    feature_cols = FeatureEngineer.get_feature_columns()
    X = df_fe[feature_cols]
    
    os.makedirs('models', exist_ok=True)
    
    for i in range(1, 8):
        print(f"Training Day +{i}...")
        y = df_fe['value'].shift(-i)
        X_train = X.iloc[:-i]
        y_train = y.iloc[:-i]
        
        valid_idx = X_train.dropna().index
        X_train = X_train.loc[valid_idx]
        y_train = y_train.loc[valid_idx]
        
        model = xgb.XGBRegressor(
            n_estimators=500, learning_rate=0.05, max_depth=5,
            subsample=0.8, objective='reg:absoluteerror', random_state=42
        )
        model.fit(X_train, y_train, verbose=False)
        model.save_model(f'models/xgb_day_{i}.json')
    print("Training complete.")

if __name__ == "__main__":
    CSV_PATH = "data/raw_data.csv" 
    if os.path.exists(CSV_PATH):
        ingest_csv(CSV_PATH)
    train_models()
