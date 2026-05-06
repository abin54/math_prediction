import pandas as pd
from src.model import DailyPredictor
import os

def main():
    # Load the cleaned sandbox data as source
    data_path = "daily_predictor/data.csv"
    if not os.path.exists(data_path):
        print("Historical data not found. Run scripts/format_sandbox_csv.py first.")
        return

    print("Loading 52-year dataset...")
    df = pd.read_csv(data_path)
    df.columns = ['ds', 'value']
    
    predictor = DailyPredictor()
    
    print("Initiating Production Training (Chronological Split)...")
    metrics = predictor.train(df)
    
    print("\n" + "="*40)
    print("PRODUCTION TRAINING COMPLETE")
    print(f"MAE: {metrics['MAE']:.4f}")
    print(f"MAPE: {metrics['MAPE']:.4%}")
    print("="*40)
    print("Model saved to models/latest_model.json")

if __name__ == "__main__":
    main()
