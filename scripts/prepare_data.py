import pandas as pd
import numpy as np
from pathlib import Path

def prepare_forecasting_data(csv_path: str):
    """
    Cleans the 52-year dataset and prepares it for Prophet, NeuralForecast, and Chronos.
    """
    df = pd.read_csv(csv_path)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Clean missing data (* and XX)
    # We focus on the 'Open' digit as the target 'y'
    df['y'] = pd.to_numeric(df['Open'], errors='coerce')
    
    # Drop rows with missing target or date
    df = df.dropna(subset=['Date', 'y'])
    
    # Sort by date
    df = df.sort_values('Date')
    
    # Prepare Prophet format
    prophet_df = df[['Date', 'y']].rename(columns={'Date': 'ds'})
    
    # Prepare NeuralForecast format
    nf_df = prophet_df.copy()
    nf_df['unique_id'] = 'sovereign_series'
    
    # Prepare Chronos format (raw numpy array)
    chronos_data = nf_df['y'].values
    
    return prophet_df, nf_df, chronos_data

if __name__ == "__main__":
    csv_path = "data/constitutional_master_v52.csv"
    p_df, n_df, c_data = prepare_forecasting_data(csv_path)
    print(f"Data prepared: {len(p_df)} valid nodes found.")
    
    # Save processed data for easy loading by model scripts
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    p_df.to_csv("data/processed/prophet_data.csv", index=False)
    n_df.to_csv("data/processed/neuralforecast_data.csv", index=False)
    np.save("data/processed/chronos_data.npy", c_data)
