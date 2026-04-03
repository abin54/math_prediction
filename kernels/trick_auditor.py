import pandas as pd
import numpy as np
import os
from collections import Counter

MIRROR = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}

def get_total(v):
    try:
        v = int(pd.to_numeric(v, errors='coerce'))
        return (v // 10 + v % 10) % 10
    except:
        return -1

def audit_tricks():
    file = "Number_Chart.xlsx"
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    
    tricks = {
        "Total Repeat": 0,
        "Mirror Repeat": 0,
        "Unit Lock": 0,
        "Step-3 Total": 0,
        "Family Continuity": 0,
        "Total Count": 0
    }
    
    # Audit last 200 weeks
    data = df.tail(200)
    
    for i in range(len(data) - 1):
        # We check MON -> TUE transition as a sample
        v1 = data.iloc[i]['MON Jodi Num']
        v2 = data.iloc[i]['TUE Jodi Num']
        
        if pd.isna(v1) or pd.isna(v2): continue
        
        v1, v2 = int(v1), int(v2)
        t1, u1 = v1 // 10, v1 % 10
        t2, u2 = v2 // 10, v2 % 10
        tot1, tot2 = get_total(v1), get_total(v2)
        
        tricks["Total Count"] += 1
        
        # 1. Total Repeat
        if tot1 == tot2: tricks["Total Repeat"] += 1
        
        # 2. Mirror Repeat (Digit mirror)
        if t2 == MIRROR[t1] or t2 == MIRROR[u1] or u2 == MIRROR[t1] or u2 == MIRROR[u1]:
            tricks["Mirror Repeat"] += 1
            
        # 3. Unit Lock
        if u1 == u2: tricks["Unit Lock"] += 1
        
        # 4. Step-3 Logic (+3 progression)
        if (tot1 + 3) % 10 == tot2: tricks["Step-3 Total"] += 1

    print("\n" + "="*50)
    print("  HISTORICAL TRICK AUDIT (Last 200 Weeks)")
    print("="*50)
    for k, v in tricks.items():
        if k == "Total Count": continue
        pct = (v / tricks["Total Count"]) * 100
        print(f"  {k:20}: {v:3} hits ({pct:.1f}%)")
    print("="*50)

if __name__ == "__main__":
    audit_tricks()
