import pandas as pd
import os

def get_total(v):
    try:
        v = int(pd.to_numeric(v, errors='coerce'))
        return (v // 10 + v % 10) % 10
    except:
        return -1

def search():
    file = "Number_Chart.xlsx"
    if not os.path.exists(file):
        print("File not found.")
        return
        
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    
    df['MT'] = df['MON Jodi Num'].apply(get_total)
    df['TT'] = df['TUE Jodi Num'].apply(get_total)
    df['WT'] = df['WED Jodi Num'].apply(get_total)
    
    # Filter for MON Total 1 and TUE Total 4
    mask = (df['MT'] == 1) & (df['TT'] == 4)
    matches = df[mask]
    
    print(f"Total Matches for MON(T1) -> TUE(T4): {len(matches)}")
    print("-" * 50)
    
    for idx, row in matches.iterrows():
        # Exclude current week if present
        if str(row['Date Range']).strip() == "30/03/2026 \nto \n04/04/2026":
            continue
            
        print(f"Week: {row['Date Range'].replace('\\n', ' ')}")
        print(f"  MON: {row['MON Jodi Num']} (Total 1)")
        print(f"  TUE: {row['TUE Jodi Num']} (Total 4)")
        print(f"  WED: {row['WED Jodi Num']} (Total {row['WT']})")
        print("-" * 30)

if __name__ == "__main__":
    search()
