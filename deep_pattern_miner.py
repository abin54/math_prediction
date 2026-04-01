"""
Deep Pattern Miner — Specialized Wednesday "Tricks" (Anchor: 74 -> 04)
=====================================================================
Analyzes the (74 -> 04) sequence for Wednesday predictions.
Since 74 -> 04 is a rare sequence, we use:
1. Total Progression (1 -> 4 -> ?)
2. Family Sequence Matching
3. Digit Repetition Logic
"""

import pandas as pd
import numpy as np
import os
from collections import Counter

# CONFIG
CHART_FILE = "Number_Chart.xlsx"
DATASET_FILE = "Kalyan_Panel_Chart_Dataset.xlsx"
MON_VAL = 74
TUE_VAL = 4

MIRROR = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}

def get_family(n):
    t, u = n // 10, n % 10
    mt, mu = MIRROR[t], MIRROR[u]
    return sorted(list({t*10+u, t*10+mu, mt*10+u, mt*10+mu, u*10+t, u*10+mt, mu*10+t, mu*10+mt}))

def load_data():
    all_trios = []
    if os.path.exists(CHART_FILE):
        df = pd.read_excel(CHART_FILE, sheet_name="Numeric Analysis", header=0)
        cols = ["MON Jodi Num", "TUE Jodi Num", "WED Jodi Num"]
        if all(c in df.columns for c in cols):
            valid = df[cols].dropna().astype(int)
            for _, row in valid.iterrows():
                all_trios.append((row[cols[0]], row[cols[1]], row[cols[2]]))
    return all_trios

def mine_deep_logic():
    print("\n" + "="*75)
    print("  DEEP PATTERN MINER — WEDNESDAY TRICKS (AFTER 74 -> 04)")
    print("="*75)
    
    trios = load_data()
    if not trios:
        print("  ! No historical data found.")
        return
        
    df = pd.DataFrame(trios, columns=['MON', 'TUE', 'WED'])
    
    # 1. TOTAL PROGRESSION (TP)
    print(f"\n  [TRICK 1] Total Progression (TP) Logic")
    print(f"  --------------------------------------")
    mon_tp = (MON_VAL // 10 + MON_VAL % 10) % 10
    tue_tp = (TUE_VAL // 10 + TUE_VAL % 10) % 10
    print(f"    - Sequence Totals: MON={mon_tp}, TUE={tue_tp}")
    
    tp_matches = df[((df['MON'] // 10 + df['MON'] % 10) % 10 == mon_tp) & 
                    ((df['TUE'] // 10 + df['TUE'] % 10) % 10 == tue_tp)]
    
    if not tp_matches.empty:
        wed_totals = Counter((v // 10 + v % 10) % 10 for v in tp_matches['WED'])
        top_tp, cnt = wed_totals.most_common(1)[0]
        print(f"    - Historical WED Totals after (Total {mon_tp} -> {tue_tp}): {top_tp} ({cnt}x)")
        print(f"    - TRICK Suggests: Numbers with Total {top_tp}")
    else:
        # Fallback to TUE Total 4 only
        wed_totals = Counter((v // 10 + v % 10) % 10 for v in df[((df['TUE'] // 10 + df['TUE'] % 10) % 10 == tue_tp)]['WED'])
        top_tp, cnt = wed_totals.most_common(1)[0]
        print(f"    - Secondary WED Totals after (Total {tue_tp}): {top_tp} ({cnt}x)")

    # 2. FAMILY SEQUENCE
    print(f"\n  [TRICK 2] Family Sequence Matching")
    print(f"  ---------------------------------")
    mon_fam = get_family(MON_VAL)
    tue_fam = get_family(TUE_VAL)
    
    fam_matches = df[df['MON'].isin(mon_fam) & df['TUE'].isin(tue_fam)]
    if not fam_matches.empty:
        wed_vals = Counter(fam_matches['WED'])
        print(f"    - Family matches found: {len(fam_matches)}")
        print(f"    - Top Wednesday results in this family sequence:")
        for v, c in wed_vals.most_common(4):
            print(f"      {v:02d} ({c}x)")
    else:
        print("    - No historical family sequence match found.")

    # 3. UNIT REPETITION (4 -> 4 -> ?)
    print(f"\n  [TRICK 3] Units Digit Repetition (4 -> 4 -> ?)")
    print(f"  ---------------------------------------------")
    rep_matches = df[(df['MON'] % 10 == 4) & (df['TUE'] % 10 == 4)]
    if not rep_matches.empty:
        wed_units = Counter(rep_matches['WED'] % 10)
        top_u, cnt = wed_units.most_common(1)[0]
        print(f"    - When Units repeat (4 -> 4), the next Wednesday Unit is often: {top_u} ({cnt}x)")
    else:
        print("    - No repeat matches (4->4) found.")

    # 4. CROSS-DAY MIRRORS
    print(f"\n  [TRICK 4] Cross-Day Mirror/Cut Calculation")
    print(f"  -----------------------------------------")
    print(f"    - MON: 7, 4")
    print(f"    - TUE: 0, 4 (Repeat 4, Mirror 7 partially? No, 7 is 2 in mirror)")
    # Logic: 0 is related to 7 in some cycles (7-0-3-6-9)
    print(f"    - Cycle Logic Suggests: WED might have 3 or 7 (Progression of 3).")

    print("\n" + "="*75)
    print("  TRICK CONSOLIDATION — FINAL WEDNESDAY SCORECARD")
    print("="*75)
    
    scores = Counter()
    # Boost by TP
    # Historical TP after (1->4) suggests Totals.
    # From miner: Top WED Total is 0 (23x in previous run).
    # Common 0-total Jodis: 19, 55, 28, 37, 46, 00, 19...
    for v in [19, 55, 28, 37, 46, 00, 91]:
        scores[v] += 12
        
    # Boost by Family sequence (If matches were found)
    # If no exact family sequence, use the Family of 04
    for v in [59, 95, 9, 45, 54, 40, 90, 4]:
        scores[v] += 8
        
    # Boost by Unit Repetition (Top unit from rep_matches)
    if not rep_matches.empty:
        top_unit = top_u
        for v in range(10):
            scores[v * 10 + top_unit] += 10

    # Final Choices
    top_picks = scores.most_common(5)
    for i, (v, s) in enumerate(top_picks):
        print(f"  TRICK CHOICE #{i+1}: {v:02d} (Confidence: {s})")
    print("\n" + "="*75)

if __name__ == "__main__":
    mine_deep_logic()
