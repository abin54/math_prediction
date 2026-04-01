import pandas as pd
import os

MIRROR = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}

def get_total(v):
    try:
        v = int(pd.to_numeric(v, errors='coerce'))
        return (v // 10 + v % 10) % 10
    except:
        return -1

def analyze_mirror_logic():
    file = "Number_Chart.xlsx"
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    
    df['MT'] = df['MON Jodi Num'].apply(get_total)
    df['TT'] = df['TUE Jodi Num'].apply(get_total)
    df['WT'] = df['WED Jodi Num'].apply(get_total)
    
    # Mirror of this week's 1 -> 4 progression is 6 -> 9
    print("\n" + "="*70)
    print("  MIRROR LOGIC ANALYSIS (Total 6 -> 9 Sequence)")
    print("="*70)
    
    mask = (df['MT'] == 6) & (df['TT'] == 9)
    matches = df[mask]
    
    print(f"Total Mirror Matches Found (Total 6 -> 9): {len(matches)}")
    print("-" * 50)
    
    for idx, row in matches.iterrows():
        print(f"Week: {row['Date Range'].replace('\\n', ' ')}")
        print(f"  MON: {row['MON Jodi Num']} (Total 6)")
        print(f"  TUE: {row['TUE Jodi Num']} (Total 9)")
        print(f"  WED: {row['WED Jodi Num']} (Total {row['WT']})")
        print("-" * 30)

    # Also check if 29 -> 59 (Direct Mirror of 74 -> 04) ever happened
    print("\n" + "="*70)
    print("  DIRECT JODI MIRROR SEARCH (29 -> 59 Sequence)")
    print("="*70)
    
    mask2 = (df['MON Jodi Num'] == 29) & (df['TUE Jodi Num'] == 59)
    matches2 = df[mask2]
    print(f"Total Jodi Mirror Matches Found: {len(matches2)}")
    if not matches2.empty:
        for idx, row in matches2.iterrows():
            print(f"Row {idx}: 29 -> 59 leads to WED {row['WED Jodi Num']}")

if __name__ == "__main__":
    analyze_mirror_logic()
