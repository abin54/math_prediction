"""
Master Dataset Auditor v1.0 — 10-Point Forensic Audit
=====================================================
Performs advanced statistical and algorithmic tests on the 52-year dataset
to identify hidden "Logical DNA" and non-obvious "Edges".
"""

import pandas as pd
import numpy as np
from collections import Counter, defaultdict
from scipy import stats
import os

# CONFIG
CHART_FILE = "Number_Chart.xlsx"
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]

def get_week_of_month(date_str):
    """Calculates the week of the month (1-5)."""
    import re
    try:
        m = re.search(r'(\d{2})/', str(date_str))
        day = int(m.group(1))
        return (day - 1) // 7 + 1
    except:
        return 0

def run_audit():
    if not os.path.exists(CHART_FILE):
        print("Chart not found.")
        return
        
    df = pd.read_excel(CHART_FILE, sheet_name="Numeric Analysis")
    
    # 1. HEATMAP (Day vs Week of Month)
    print("\n" + "="*70)
    print("  1. HEATMAP: DAY vs WEEK OF MONTH (Deviation Analysis)")
    print("-" * 70)
    df['WOM'] = df['Date Range'].apply(get_week_of_month)
    global_mean = df[[f"{d} Jodi Num" for d in DAYS]].mean().mean()
    
    for wom in range(1, 6):
        subset = df[df['WOM'] == wom]
        for d in DAYS:
            wom_day_mean = subset[f"{d} Jodi Num"].mean()
            diff = wom_day_mean - global_mean
            if abs(diff) > 5.0: # Significant deviation threshold
                print(f"    [HOT!] Week {wom} {d}: Mean={wom_day_mean:.1f} (Diff: {diff:+.1f})")

    # 2. GAP ANALYSIS (Consistent Gaps)
    print("\n" + "="*70)
    print("  2. GAP ANALYSIS: TOP 10 MOST CONSISTENT")
    print("-" * 70)
    sequence = []
    for idx, row in df.iterrows():
        for d in DAYS:
            v = row[f"{d} Jodi Num"]
            if not pd.isna(v): sequence.append(int(v))
            
    gap_data = defaultdict(list)
    last_seen = {}
    for i, v in enumerate(sequence):
        if v in last_seen:
            gap_data[v].append(i - last_seen[v])
        last_seen[v] = i
        
    consistencies = []
    for v, gaps in gap_data.items():
        if len(gaps) > 10:
            std_gap = np.std(gaps)
            avg_gap = np.mean(gaps)
            consistencies.append((v, avg_gap, std_gap))
            
    consistencies.sort(key=lambda x: x[2]) # Sort by Std Dev (most consistent)
    for v, avg, std in consistencies[:10]:
        print(f"    Number {v:02}: Avg Gap = {avg:.1f} days (Std Dev: {std:.1f})")

    # 3. BENFORD'S LAW (First Digits / Tens)
    print("\n" + "="*70)
    print("  3. BENFORD'S LAW TEST (Tens Digits)")
    print("-" * 70)
    tens = [v // 10 for v in sequence if v >= 10]
    tens_counts = Counter(tens)
    n_tens = len(tens)
    for d in range(1, 10):
        obs = tens_counts.get(d, 0) / n_tens
        exp = np.log10(1 + 1/d)
        print(f"    Digit {d}: Observed={obs:.1%} | Expected={exp:.1%}")

    # 4. MARKOV TRANSITION MATRIX (Strong Links)
    print("\n" + "="*70)
    print("  4. MARKOV TRANSITIONS: SEARCHING FOR >20% LINKS")
    print("-" * 70)
    # 60% might be too high for 100 choices, checking >20%
    transitions = defaultdict(Counter)
    for i in range(len(sequence)-1):
        transitions[sequence[i]][sequence[i+1]] += 1
        
    strong_links = []
    for a, targets in transitions.items():
        total_a = sum(targets.values())
        for b, count in targets.items():
            prob = count / total_a
            if prob > 0.20:
                strong_links.append((a, b, prob))
                
    strong_links.sort(key=lambda x: -x[2])
    for a, b, prob in strong_links[:10]:
        print(f"    {a:02} -> {b:02}: Link Strength = {prob:.1%}")

    # 5. REGIME SHIFT (Decade Comparisons)
    print("\n" + "="*70)
    print("  5. REGIME SHIFT: DECADE-BY-DECADE VAR/MEAN")
    print("-" * 70)
    import re
    def get_yr(s):
        try: m = re.search(r'/(\d{4})', str(s)); return int(m.group(1))
        except: return 0
    df['Year'] = df['Date Range'].apply(get_yr)
    
    for decade in range(1970, 2030, 10):
        subset = df[(df['Year'] >= decade) & (df['Year'] < decade + 10)]
        if not subset.empty:
            dec_seq = []
            for d in DAYS:
                dec_seq.extend(subset[f"{d} Jodi Num"].dropna().tolist())
            print(f"    Decade {decade}s: Mean={np.mean(dec_seq):.1f} | Var={np.var(dec_seq):.1f}")

    print("\n" + "="*70)

if __name__ == "__main__":
    run_audit()
