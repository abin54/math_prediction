"""
Historical Trick Miner v1.0 — Pattern Archaeology
===============================================
1. Scans every day from 2012 to 2026.
2. Reverse-engineers the "Logic" of Day(N) based on Day(N-1).
3. Generates a 'Trick Heatmap' showing which logic hits most often.
"""

import pandas as pd
import numpy as np
import os, json
from collections import Counter

# Mirror map: 0->5, 1->6, 2->7, 3->8, 4->9
MIRROR = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}

def get_mirror_set(n):
    t, u = n // 10, n % 10
    return sorted(list({
        # Full, Mirror-Open, Mirror-Close, Both
        n,
        MIRROR[t]*10 + u,
        t*10 + MIRROR[u],
        MIRROR[t]*10 + MIRROR[u]
    }))

def run_archeologist():
    print("\n" + "="*80)
    print("  HISTORICAL PATTERN ARCHEOLOGY: 14-YEAR SCAN (2012-2026)")
    print("="*80)
    
    # Load dataset
    df = pd.read_excel("Number_Chart.xlsx", sheet_name="Numeric Analysis")
    results_flat = []
    
    # Prepare a flat chronological sequence of Jodis
    for i in range(len(df)):
        for day in ["MON", "TUE", "WED", "THU", "FRI", "SAT"]:
            col = f"{day} Jodi Num"
            if col in df.columns and not pd.isna(df.iloc[i][col]):
                results_flat.append(int(df.iloc[i][col]))
                
    if not results_flat:
        print("  [ERROR] No data found in Number_Chart.xlsx.")
        return

    print(f"  Scanning {len(results_flat)} cumulative days...")
    
    trick_log = []
    
    for i in range(1, len(results_flat)):
        prev = results_flat[i-1]
        curr = results_flat[i]
        
        p_t, p_u = prev // 10, prev % 10
        c_t, c_u = curr // 10, curr % 10
        
        tricks_detected = []
        
        # 1. Mirror Logic
        if curr in get_mirror_set(prev):
            tricks_detected.append("Mirror/Family")
            
        # 2. Step Logic (Open)
        diff_open = (c_t - p_t) % 10
        if diff_open in [1, 2, 9, 8]:
            tricks_detected.append(f"Open-Step-{diff_open}")
            
        # 3. Sum / Total Logic
        if (p_t + p_u) % 10 == c_t or (p_t + p_u) % 10 == c_u:
            tricks_detected.append("Sum-Total-Echo")
            
        # 4. Same Digit (Open Repeat)
        if c_t == p_t:
            tricks_detected.append("Repeat-Open")
            
        # 5. Same Digit (Close Repeat)
        if c_u == p_u:
            tricks_detected.append("Repeat-Close")
            
        if tricks_detected:
            trick_log.extend(tricks_detected)

    # Summarize results
    stats = Counter(trick_log)
    print("\n  [ULTIMATE TRICK HEATMAP]:")
    total_samples = len(results_flat) - 1
    
    heatmap_data = {}
    for trick, count in stats.most_common(15):
        freq = count / total_samples
        print(f"    - {trick:18}: {count:4} hits ({freq:.1%})")
        heatmap_data[trick] = freq

    with open("learned_tricks.json", "w") as f:
        json.dump(heatmap_data, f, indent=4)
        
    print(f"\n  [SUCCESS] learned_tricks.json generated.")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_archeologist()
