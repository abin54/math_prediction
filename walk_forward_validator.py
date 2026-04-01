"""
Walk-Forward Validator v1.0 — 2016-2020 Stress Test
===================================================
Simulates the years 2016 to 2020 by predicting week-by-week
using ONLY preceding data for each week.
"""

import pandas as pd
import numpy as np
from collections import Counter

# CONFIG
MIRROR = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}
VALIDATION_RANGE = (151, 481) # 2016 to 2020 Indices

def get_total(v):
    try:
        v = int(pd.to_numeric(v, errors='coerce'))
        return (v // 10 + v % 10) % 10
    except:
        return -1

def get_family(n):
    t, u = n // 10, n % 10
    mt, mu = MIRROR[t], MIRROR[u]
    return {t*10+u, t*10+mu, mt*10+u, mt*10+mu, u*10+t, u*10+mt, mu*10+t, mu*10+mt}

def predict_week(history_df, target_mon, target_tue):
    """Simple Logic Agent for WFV (Mirror + Step-3 + Freq)."""
    # 1. Stat Logic (Top 10 Freq)
    all_vals = history_df['MON Jodi Num'].dropna().astype(int).tolist() + \
               history_df['TUE Jodi Num'].dropna().astype(int).tolist()
    freq_top = [v for v, c in Counter(all_vals).most_common(5)]
    
    # 2. Mirror Logic (based on MON)
    mon_jodi = int(target_mon) if not pd.isna(target_mon) else -1
    mirror_picks = []
    if mon_jodi != -1:
        t, u = mon_jodi // 10, mon_jodi % 10
        mirror_picks = [MIRROR[t]*10+u, t*10+MIRROR[u], MIRROR[t]*10+MIRROR[u]]
        
    # 3. Step-3 Logic (based on MON total)
    step_picks = []
    if mon_jodi != -1:
        mon_tot = get_total(mon_jodi)
        target_tot = (mon_tot + 3) % 10
        # Find some candidates with this total
        for i in range(100):
            if get_total(i) == target_tot:
                step_picks.append(i)
                if len(step_picks) >= 3: break
                
    # Ensemble
    candidates = list(set(freq_top + mirror_picks + step_picks))
    return candidates[:10]

def analyze_failure(mon_jodi, actual_tue, candidates):
    """Categorize why we missed."""
    if pd.isna(mon_jodi) or pd.isna(actual_tue): return "SKIP"
    
    mon_jodi, actual_tue = int(mon_jodi), int(actual_tue)
    t1, u1 = mon_jodi // 10, mon_jodi % 10
    t2, u2 = actual_tue // 10, actual_tue % 10
    
    # Mirror Break
    if not (t2 == MIRROR[t1] or t2 == MIRROR[u1] or u2 == MIRROR[t1] or u2 == MIRROR[u1]):
        return "MIRROR-BREAK"
        
    # Step Shift
    tot1, tot2 = get_total(mon_jodi), get_total(actual_tue)
    if (tot1 + 3) % 10 != tot2 and (tot1 + 7) % 10 != tot2:
        return "STEP-SHIFT"
        
    return "LOGIC-FADE"

def run_wfv():
    df = pd.read_excel("Number_Chart.xlsx", sheet_name="Numeric Analysis")
    
    hits = 0
    total_valid = 0
    failures = []
    
    print(f"Starting WFV for weeks {VALIDATION_RANGE[0]} to {VALIDATION_RANGE[1]}...")
    
    for i in range(VALIDATION_RANGE[0], VALIDATION_RANGE[1] + 1):
        history = df.iloc[:i]
        target_row = df.iloc[i]
        
        mon_val = target_row['MON Jodi Num']
        actual_tue = target_row['TUE Jodi Num']
        
        if pd.isna(mon_val) or pd.isna(actual_tue):
            continue
            
        total_valid += 1
        preds = predict_week(history, mon_val, actual_tue)
        
        if int(actual_tue) in preds:
            hits += 1
        else:
            reason = analyze_failure(mon_val, actual_tue, preds)
            failures.append({
                "Date": target_row['Date Range'],
                "MON": mon_val,
                "TUE": actual_tue,
                "Reason": reason
            })
            
    # RESULTS
    print("\n" + "="*50)
    print("  WALK-FORWARD VALIDATION RESULTS (2016-2020)")
    print("="*50)
    accuracy = (hits / total_valid) * 100 if total_valid > 0 else 0
    print(f"  Total Weeks Validated: {total_valid}")
    print(f"  Total Hits @ Top-10  : {hits}")
    print(f"  Overall Accuracy     : {accuracy:.1f}%")
    print("="*50)
    
    # Report failures
    with open("wfv_failure_log.txt", "w") as f:
        f.write("FAILURE ANALYSIS LOG: 2016-2020\n")
        f.write("================================\n\n")
        for fail in failures:
            f.write(f"Date: {fail['Date'].replace('\\n', ' ')}\n")
            f.write(f"  MON: {fail['MON']} -> TUE: {fail['TUE']}\n")
            f.write(f"  Failure Category: {fail['Reason']}\n")
            f.write("-" * 40 + "\n")

if __name__ == "__main__":
    run_wfv()
