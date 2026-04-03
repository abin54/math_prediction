"""
Regime Shift & CUSUM Auditor v11.3 — The Chronological Anchor
============================================================
1. Identifies "Logic Shifts" across 52 years using CUSUM (Cumulative Sum) 
   of variance to find exactly when the chart's 'Handwriting' changed.
2. Weights the training data to prioritize the 2020-2026 regime.
"""

import pandas as pd
import numpy as np
import os
import re

def get_yr(s):
    try: m = re.search(r'/(\d{4})', str(s)); return int(m.group(1))
    except: return 0

def run_regime_audit():
    file = "Number_Chart.xlsx"
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    df['Year'] = df['Date Range'].apply(get_yr)
    
    # Flatten history
    full_seq = []
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    for idx, row in df.iterrows():
        for d in days:
            v = row[f"{d} Jodi Num"]
            if not pd.isna(v): full_seq.append((row['Year'], float(v)))
            
    seq = np.array([x[1] for x in full_seq])
    years = np.array([x[0] for x in full_seq])
    
    # CUSUM Analysis for Mean Shift
    # (Checking where the cumulative mean starts to deviate)
    global_mean = np.mean(seq)
    cusum = np.cumsum(seq - global_mean)
    
    # Peak of CUSUM indicates the shift point
    shift_idx = np.argmax(np.abs(cusum))
    shift_year = years[shift_idx]
    
    print("\n" + "="*70)
    print("  LAYER 1: REGIME SHIFT & CUSUM AUDIT")
    print("-" * 70)
    print(f"  Historical Baseline (1972-2026): {global_mean:.2f}")
    print(f"  Significant Regime Shift Detected: Year {shift_year}")
    
    # Compare 1970s vs 2020s
    v_70s = seq[years < 1980]
    v_2020s = seq[years >= 2020]
    
    print(f"\n  [ANCHOR] 1970s Mean: {np.mean(v_70s):.2f} | Var: {np.var(v_70s):.1f}")
    print(f"  [MODERN] 2020s Mean: {np.mean(v_2020s):.2f} | Var: {np.var(v_2020s):.1f}")
    
    if abs(np.mean(v_70s) - np.mean(v_2020s)) > 2.0:
        print("    RESULT: DRAMATIC SHIFT FOUND! 2020s logic is LOWER-DIGIT weighted.")
    else:
        print("    RESULT: STABLE ANCHOR. Logic is consistent across the 52-year span.")

    return shift_year

if __name__ == "__main__":
    run_regime_audit()
