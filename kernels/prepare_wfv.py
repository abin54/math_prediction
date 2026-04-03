import pandas as pd
import re

def get_year(s):
    try:
        # Match dd/mm/yyyy or dd/mm/yy
        m = re.search(r'\d{2}/\d{2}/(\d{2,4})', str(s))
        if not m: return 0
        y_str = m.group(1)
        if len(y_str) == 2:
            y = int(y_str)
            # Threshold 50: 50-99 -> 19XX, 00-49 -> 20XX
            return 1900 + y if y > 50 else 2000 + y
        return int(y_str)
    except:
        return 0

def prepare():
    file = "Number_Chart.xlsx"
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    df['Year'] = df['Date Range'].apply(get_year)
    
    # 1. Training Set: 1972 to 2015
    train_mask = (df['Year'] >= 1972) & (df['Year'] <= 2015)
    train_indices = df[train_mask].index.tolist()
    
    # 2. Validation Set: 2016 to 2020
    val_mask = (df['Year'] >= 2016) & (df['Year'] <= 2020)
    val_indices = df[val_mask].index.tolist()
    
    print(f"Training Index Range: {train_indices[0]} to {train_indices[-1]} (Count: {len(train_indices)})")
    print(f"Validation Index Range: {val_indices[0]} to {val_indices[-1]} (Count: {len(val_indices)})")
    
    # Check if there are any results in the validation set
    sample_val = df.loc[val_indices].head(5)
    print("\nSample Validation Data:")
    print(sample_val[['Date Range', 'MON Jodi Num', 'TUE Jodi Num']])

if __name__ == "__main__":
    prepare()
