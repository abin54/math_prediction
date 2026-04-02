
import pandas as pd
import numpy as np
from collections import Counter

EXCEL_FILE = "Number_Chart.xlsx"
SHEET_NAME = "Numeric Analysis"
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]

def analyze_week_pattern():
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    
    # 1. Transition Analysis: WED -> THU
    wed_vals = df["WED Jodi Num"].dropna().astype(int).tolist()
    thu_vals = df["THU Jodi Num"].dropna().astype(int).tolist()
    
    # Yesterday (WED) was 19
    yesterday_wed = 19
    
    print(f"--- Analysis for Wednesday 19 -> Thursday ---")
    
    # Find all occurrences of WED 19
    indices = [i for i, x in enumerate(wed_vals) if x == yesterday_wed]
    followers = []
    for idx in indices:
        if idx < len(thu_vals):
            followers.append(thu_vals[idx])
    
    if followers:
        print(f"Historical followers of WED 19 on THU: {followers}")
        c = Counter(followers)
        print(f"Most common: {c.most_common(3)}")
    else:
        print("No historical exact match for WED 19 followed by THU.")

    # 2. Family / Mirror Analysis for 19
    # 1 -> 6 (mirror), 9 -> 4 (mirror)
    # Family of 19: 19, 14, 69, 64, 91, 41, 96, 46
    family_19 = [19, 14, 69, 64, 91, 41, 96, 46]
    family_followers = []
    for f_val in family_19:
        f_indices = [i for i, x in enumerate(wed_vals) if x == f_val]
        for idx in f_indices:
            if idx < len(thu_vals):
                family_followers.append(thu_vals[idx])
    
    if family_followers:
        print(f"\nHistorical followers of WED 19's Family on THU: {len(family_followers)} matches")
        c_fam = Counter(family_followers)
        print(f"Top 5: {c_fam.most_common(5)}")

    # 3. This week's sequence: 74 (MON) -> 04 (TUE) -> 19 (WED)
    # Sequence of Open digits: 7 -> 0 -> 1
    # Sequence of Close digits: 4 -> 4 -> 9
    
    print(f"\n--- This Week's Pattern ---")
    print(f"MON: 74")
    print(f"TUE: 04 (Mirror of Open 7 is 2, Cut is 2... 0 is? 7-7=0?)")
    print(f"WED: 19 (Open: 0+1=1, Close: 4 mirror=9)")
    
    # Predictive logic for THU:
    # Open: 7 -> 0 -> 1 -> ? (0+1=1, maybe 1+1=2? or 1+2=3?)
    # Close: 4 -> 4 -> 9 -> ? (Repeat 4, then mirror 9, maybe repeat 9 or mirror 4?)
    
    potential_open = [2, 3, 6] # 1+1, 1+2, 1 mirror
    potential_close = [4, 9, 3] # 9 mirror, 9 repeat, 4-1?
    
    print(f"\nPotential THU Jodis based on Logic:")
    print(f"- Progression (+1): 2 (Open) -> 24, 29")
    print(f"- Mirror/Repeat: 64, 69")
    print(f"- Open Step (+2): 34, 39")

if __name__ == "__main__":
    analyze_week_pattern()
