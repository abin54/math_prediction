
import pandas as pd
from collections import Counter

EXCEL_FILE = "Number_Chart.xlsx"

def analyze_double_open():
    df = pd.read_excel(EXCEL_FILE, sheet_name="Numeric Analysis")
    wed = df["WED Jodi Num"].dropna().astype(int).tolist()
    thu = df["THU Jodi Num"].dropna().astype(int).tolist()
    
    min_len = min(len(wed), len(thu))
    
    matches = []
    for i in range(min_len):
        if wed[i] // 10 == 1:
            if i < len(thu) and thu[i] // 10 == 1:
                matches.append(thu[i])
                
    print(f"\nHistorical Thursdays with OPEN 1 following a WED OPEN 1: {len(matches)}")
    if matches:
        c = Counter(matches)
        print(f"Most common Jodi: {c.most_common(5)}")
        
    # Check for WED 19 specifically
    matches_19 = []
    for i in range(min_len):
        if wed[i] == 19:
            if i < len(thu) and thu[i] // 10 == 1:
                matches_19.append(thu[i])
                
    print(f"\nHistorical Thursdays with OPEN 1 following WED 19: {len(matches_19)}")
    if matches_19:
        print(f"Jodis: {matches_19}")

if __name__ == "__main__":
    analyze_double_open()
