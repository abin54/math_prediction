import pandas as pd
import xgboost as xgb
import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import SessionLocal, DailyValue
from src.features import FeatureEngineer

def ingest_csv(csv_path: str):
    print(f"Ingesting {csv_path} into database...")
    df = pd.read_csv(csv_path)
    # The sandbox dataset has Date and Open columns
    # We map them to date and value
    if 'Date' in df.columns and 'Open' in df.columns:
        df = df[['Date', 'Open']]
        df.columns = ['date', 'value']
    elif len(df.columns) >= 2:
        df = df.iloc[:, [0, 1]]
        df.columns = ['date', 'value']
    
    df['date'] = pd.to_datetime(df['date']).dt.date
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna()
    
    db = SessionLocal()
    count = 0
    records_to_add = []
    
    # Get existing dates to avoid duplicates
    from sqlalchemy import select
    existing_dates = set(db.execute(select(DailyValue.date)).scalars().all())
    
    for _, row in df.iterrows():
        if row['date'] not in existing_dates:
            records_to_add.append(DailyValue(date=row['date'], value=row['value']))
            existing_dates.add(row['date']) # Add to set to avoid duplicates in same batch
            count += 1
            if len(records_to_add) >= 1000:
                db.bulk_save_objects(records_to_add)
                records_to_add = []
                
    if records_to_add:
        db.bulk_save_objects(records_to_add)
        
    db.commit()
    db.close()
    print(f"Added {count} new records to DB.")

def train_models():
    print("Pulling data from DB and engineering features...")
    from src.database import get_historical_df
    df = get_historical_df(days=20000) # Get all 52 years
    df_fe = FeatureEngineer.build_features(df)
    
    feature_cols = FeatureEngineer.get_feature_columns()
    X = df_fe[feature_cols]
    
    # Ensure models directory exists
    os.makedirs('models', exist_ok=True)
    
    print("Training 7 Direct Multi-Step Models...")
    for i in range(1, 8):
        print(f"Training Model for Day +{i}...")
        # The target for Day +i is the value i days in the future
        y = df_fe['value'].shift(-i)
        
        # Drop last i rows because they don't have a future target
        X_train = X.iloc[:-i]
        y_train = y.iloc[:-i]
        
        # Drop any remaining NaNs
        valid_idx = X_train.dropna().index
        X_train = X_train.loc[valid_idx]
        y_train = y_train.loc[valid_idx]
        
        model = xgb.XGBRegressor(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=5,
            subsample=0.8,
            objective='reg:absoluteerror',
            random_state=42
        )
        
        model.fit(X_train, y_train, verbose=False)
        model.save_model(f'models/xgb_day_{i}.json')
        
    print("All 7 models trained and saved to /models")

if __name__ == "__main__":
    # Use the established 52-year baseline
    CSV_PATH = "daily_predictor/data.csv" 
    
    if os.path.exists(CSV_PATH):
        ingest_csv(CSV_PATH)
    else:
        print("Baseline CSV not found, checking data/raw_data.csv...")
        CSV_PATH = "data/raw_data.csv"
        if os.path.exists(CSV_PATH):
            ingest_csv(CSV_PATH)
        else:
            print("No source CSV found. Skipping ingestion.")
        
    train_models()
