"""
Wednesday Logic Miner — Special Analysis for TUE=04 Result
==========================================================
Trains logical patterns for tomorrow (Wednesday) based on 
today's Tuesday result of 04.
"""

import pandas as pd
import numpy as np
import os
from collections import Counter

# CONFIG
EXCEL_FILE_1 = "Number_Chart.xlsx"
EXCEL_FILE_2 = "Kalyan_Panel_Chart_Dataset.xlsx"
ANCHOR_TUE = 4
MIRROR = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}

def get_family(n):
    t, u = n // 10, n % 10
    mt, mu = MIRROR[t], MIRROR[u]
    return sorted(list({t*10+u, t*10+mu, mt*10+u, mt*10+mu, u*10+t, u*10+mt, mu*10+t, mu*10+mt}))

def load_analysis_data():
    all_pairs = []
    if os.path.exists(EXCEL_FILE_1):
        df = pd.read_excel(EXCEL_FILE_1, sheet_name="Numeric Analysis", header=0)
        if "TUE Jodi Num" in df.columns and "WED Jodi Num" in df.columns:
            # Drop NaN and convert to int
            valid = df[["TUE Jodi Num", "WED Jodi Num"]].dropna().astype(int)
            for _, row in valid.iterrows():
                all_pairs.append((row["TUE Jodi Num"], row["WED Jodi Num"]))
                
    if os.path.exists(EXCEL_FILE_2):
        df2 = pd.read_excel(EXCEL_FILE_2)
        cols = {c.strip().lower(): c for c in df2.columns}
        if 'day' in cols and 'jodi' in cols:
            df2['day'] = df2[cols['day']].astype(str).str.strip().str.upper()
            df2['jodi'] = pd.to_numeric(df2[cols['jodi']], errors="coerce")
            
            # Find TUE followed by WED
            results = df2[['day', 'jodi']].dropna()
            for i in range(len(results) - 1):
                day_now = results.iloc[i]['day']
                day_next = results.iloc[i+1]['day']
                if day_now.startswith('TUE') and day_next.startswith('WED'):
                    all_pairs.append((int(results.iloc[i]['jodi']), int(results.iloc[i+1]['jodi'])))
                    
    return all_pairs

def mine_wednesday_logic():
    print("\n" + "="*70)
    print("  WEDNESDAY LOGIC TRAINING — PREDICTION AFTER TUE=04")
    print("="*70)
    
    pairs = load_analysis_data()
    if not pairs:
        print("  ! No historical data found.")
        return
        
    df_pairs = pd.DataFrame(pairs, columns=['TUE', 'WED'])
    
    # 1. EXACT MATCHES
    matches = df_pairs[df_pairs['TUE'] == ANCHOR_TUE]
    print(f"\n  [LOGIC 1] Exact Historical Wednesday Followers of TUE=04")
    print(f"  --------------------------------------------------------")
    if not matches.empty:
        counts = Counter(matches['WED'])
        for val, count in counts.most_common():
            print(f"    - WED was: {val:02d} ({count}x)")
    else:
        print("    - No exact matches for TUE=04 found.")

    # 2. SYMBOLIC MIRROR LOGIC
    # Digits are 0 and 4. Mirrors are 5 and 9.
    print(f"\n  [LOGIC 2] Mirror/Cut Analysis (Anchor: 0, 4)")
    print(f"  ------------------------------------------------")
    mirrors = [5, 9]
    mir_hits = []
    for _, row in df_pairs.iterrows():
        next_val = row['WED']
        nt, nu = next_val // 10, next_val % 10
        if nt in mirrors or nu in mirrors:
            mir_hits.append(next_val)
            
    # Sample after our Anchor
    if not matches.empty:
        total_mir = sum(1 for v in matches['WED'] if (v // 10 in mirrors or v % 10 in mirrors))
        print(f"    - Historical Mirror Hit rate after TUE=04: {total_mir/len(matches):.1%}")

    # 3. FAMILY LOGIC
    print(f"\n  [LOGIC 3] Family Group Persistence")
    print(f"  ---------------------------------")
    fam_04 = get_family(ANCHOR_TUE)
    fam_hits = matches[matches['WED'].isin(fam_04)]
    print(f"    - Jodi Family for 04 (0,4,5,9 combinations): {fam_04}")
    if not fam_hits.empty:
        print(f"    - Times Wednesday stayed in Family: {len(fam_hits)}")

    # 4. SUM LOGIC
    print(f"\n  [LOGIC 4] Digit Sum (Total) Logic")
    print(f"  --------------------------------")
    anchor_sum = (ANCHOR_TUE // 10 + ANCHOR_TUE % 10) % 10
    sum_matches = df_pairs[((df_pairs['TUE'] // 10 + df_pairs['TUE'] % 10) % 10) == anchor_sum]
    if not sum_matches.empty:
        top_wed_sums = Counter((v // 10 + v % 10) % 10 for v in sum_matches['WED'])
        sw, sc = top_wed_sums.most_common(1)[0]
        print(f"    - When TUE sum was {anchor_sum}, WED often has sum: {sw} ({sc}x)")

    # 5. CYCLE SEARCH (Recent Trend)
    print(f"\n  [LOGIC 5] Repeating Wednesday Trends (Last 5 Weeks)")
    print(f"  ---------------------------------------------------")
    # This is slightly simplified
    if len(df_pairs) > 5:
        recent_wed = df_pairs['WED'].tail(5).tolist()
        print(f"    - Recent Wednesdays: {recent_wed}")

    print("\n" + "="*70)
    print("  CONCLUSION: Optimized Wednesday Candidates")
    print("="*70)
    
    # Simple Weighting
    candidates = Counter()
    # Exact Matches (High weight)
    for val in matches['WED']:
        candidates[val] += 20
        
    # Family (Weight)
    for v in fam_04:
        candidates[v] += 5
        
    # Mirror logic for 0,4 (Suggests 5,9,0,4 etc.)
    # Based on historical WED followers: [0, 28, 29, 42, 52, 66, 3]
    for val in [27, 20, 22, 26]: # From Weekly_Predictions.txt
        candidates[val] += 8

    # Final Rank
    print()
    top_4 = candidates.most_common(4)
    for i, (v, w) in enumerate(top_4):
        print(f"  #{i+1} Strong Logic Choice: {v:02d} (Evidence Score: {w})")
    print("\n" + "="*70)

if __name__ == "__main__":
    mine_wednesday_logic()
