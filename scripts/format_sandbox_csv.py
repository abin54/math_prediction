import pandas as pd
import os

# Path to the source master CSV
source_csv = "data/constitutional_master_v52.csv"
target_csv = "daily_predictor/data.csv"

# Load and clean
df = pd.read_csv(source_csv)
# We need Column 1: date, Column 2: value
# Based on earlier viewing, Column 1 is 'Date' and Column 3 is 'Open'
# But let's check columns first
print(f"Source columns: {df.columns.tolist()}")

# Ensure we pick 'Date' and 'Open'
cleaned_df = df[['Date', 'Open']].copy()
cleaned_df.columns = ['date', 'value']

# Convert 'value' to numeric (handling * and XX)
cleaned_df['value'] = pd.to_numeric(cleaned_df['value'], errors='coerce')

# Drop missing
cleaned_df = cleaned_df.dropna()

# Save exactly as requested
cleaned_df.to_csv(target_csv, index=False)
print(f"Saved {len(cleaned_df)} rows to {target_csv}")
