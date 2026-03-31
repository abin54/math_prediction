"""
Matka Trick Miner — Specialized Logic Analysis
==============================================
Analyzes the dataset for traditional Matka "tricks":
1. Mirror/Cut logic (Distance of 5)
2. Family logic (Related digit groups)
3. Total (Sum of digits) patterns
4. Week-over-Week (WoW) repetition
"""

import pandas as pd
import numpy as np
import os
from collections import Counter

# CONFIG
EXCEL_FILE_1 = "Number_Chart.xlsx"
TARGET_MON = 74

# Mirror/Cut Mappings
MIRROR = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}

def get_family(n):
    """Get the 'Family' of a Jodi number."""
    # Family is usually the set of numbers made by mirroring one or both digits
    t, u = n // 10, n % 10
    mt, mu = MIRROR[t], MIRROR[u]
    family = {
        t*10 + u,      # Original
        t*10 + mu,     # Unit Mirror
        mt*10 + u,     # Tens Mirror
        mt*10 + mu,    # Both Mirror
        u*10 + t,      # Reverse Original
        u*10 + mt,     # Reverse Unit Mirror
        mu*10 + t,     # Reverse Tens Mirror
        mu*10 + mt     # Reverse Both Mirror
    }
    return sorted(list(family))

def load_data():
    if os.path.exists(EXCEL_FILE_1):
        df = pd.read_excel(EXCEL_FILE_1, sheet_name="Numeric Analysis", header=0)
        if "MON Jodi Num" in df.columns and "TUE Jodi Num" in df.columns:
            m = pd.to_numeric(df["MON Jodi Num"], errors="coerce").dropna().astype(int).tolist()
            t = pd.to_numeric(df["TUE Jodi Num"], errors="coerce").dropna().astype(int).tolist()
            return list(zip(m, t))
    return []

def analyze_tricks():
    pairs = load_data()
    if not pairs:
        print("  ! No data found.")
        return

    print("\n" + "="*70)
    print("  MATKA TRICK MINER — Historical Logic Check")
    print("="*70)

    # 1. MIRROR/CUT LOGIC
    # How often is Tuesday a Mirror of Monday?
    mirror_hits = 0
    mirror_val_hits = []
    for m, t in pairs:
        mt, mu = MIRROR[m // 10], MIRROR[m % 10]
        # Check if TUE contains mirrored digits of MON
        if (t // 10 == mt or t // 10 == mu) or (t % 10 == mt or t % 10 == mu):
            mirror_hits += 1
            if m == TARGET_MON:
                mirror_val_hits.append(t)

    print(f"\n  [TRICK 1] Mirror/Cut Accuracy")
    print(f"  -----------------------------")
    print(f"    - Over all history, {mirror_hits/len(pairs):.1%} of Tuesdays contain a 'MIRROR' digit of Monday.")
    if mirror_val_hits:
        print(f"    - Historical Tuesdays after MON=74 with mirroring: {mirror_val_hits}")

    # 2. FAMILY LOGIC
    # How often does Tuesday stay in the same 'Family' as Monday?
    family_hits = 0
    target_family = get_family(TARGET_MON)
    family_after_74 = []
    
    for m, t in pairs:
        if t in get_family(m):
            family_hits += 1
            if m == TARGET_MON:
                family_after_74.append(t)

    print(f"\n  [TRICK 2] Family Logic (Group Repetition)")
    print(f"  -----------------------------------------")
    print(f"    - {family_hits/len(pairs):.1%} of results stay within the same 'Jodi Family' week-to-week.")
    print(f"    - Family for 74 is: {target_family}")
    if family_after_74:
        print(f"    - Historical Family hits after 74: {family_after_74}")

    # 3. TOTAL (SUM) LOGIC
    # The 'Total' is the sum of the digits (mod 10)
    total_hits = Counter()
    for m, t in pairs:
        total_m = (m // 10 + m % 10) % 10
        total_t = (t // 10 + t % 10) % 10
        if m == TARGET_MON:
            total_hits[total_t] += 1

    print(f"\n  [TRICK 3] Total (Sum) Logic")
    print(f"  ---------------------------")
    if total_hits:
        top_total = total_hits.most_common(2)
        print(f"    - When MON is 74 (Total 1), TUE often has Total: {top_total[0][0]} ({top_total[0][1]}x)")

    # 4. TRICK PREDICTION FOR TODAY
    print("\n" + "="*70)
    print("  TRICK-BASED RECOMMENDATIONS FOR TODAY")
    print("="*70)
    
    # Mirror of 74 digits (7->2, 4->9)
    # Family of 74: [24, 29, 42, 47, 72, 74, 79, 92, 97]
    
    print(f"    1. Mirror Trick Suggests: 29, 92, 24, 42")
    print(f"    2. Family Trick Suggests: 79, 24, 29")
    print(f"    3. Total Trick Suggests: Numbers with sum {top_total[0][0] if total_hits else '?'}")
    print("\n" + "="*70)

if __name__ == "__main__":
    analyze_tricks()
