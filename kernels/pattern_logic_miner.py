"""
Deep Logical Pattern Miner — Jodi Prediction Logic v1.0
======================================================
Searches for specific historical evidence and logic for today's TUE prediction
after yesterday's MON=74.
"""

import pandas as pd
import numpy as np
import os
from collections import Counter

# CONFIG
EXCEL_FILE_1 = "Number_Chart.xlsx"
EXCEL_FILE_2 = "Kalyan_Panel_Chart_Dataset.xlsx"
TARGET_MON = 74

def load_all_data():
    all_data = []
    if os.path.exists(EXCEL_FILE_1):
        df = pd.read_excel(EXCEL_FILE_1, sheet_name="Numeric Analysis", header=0)
        # Combine MON and TUE pairs
        if "MON Jodi Num" in df.columns and "TUE Jodi Num" in df.columns:
            m_vals = pd.to_numeric(df["MON Jodi Num"], errors="coerce")
            t_vals = pd.to_numeric(df["TUE Jodi Num"], errors="coerce")
            valid = pd.concat([m_vals, t_vals], axis=1).dropna().astype(int)
            for _, row in valid.iterrows():
                all_data.append({'MON': row.iloc[0], 'TUE': row.iloc[1]})

    if os.path.exists(EXCEL_FILE_2):
        df2 = pd.read_excel(EXCEL_FILE_2)
        cols = {c.strip().lower(): c for c in df2.columns}
        if 'day' in cols and 'jodi' in cols:
            df2['day'] = df2[cols['day']].astype(str).str.strip().str.upper()
            df2['jodi'] = pd.to_numeric(df2[cols['jodi']], errors="coerce")
            # Group by sequential occurrences (since it's a log)
            # This is harder for a log file, so we'll look for MON followed by TUE
            mon_list = df2[df2['day'].str.startswith('MON')]['jodi'].dropna().astype(int).tolist()
            tue_list = df2[df2['day'].str.startswith('TUE')]['jodi'].dropna().astype(int).tolist()
            # If they are roughly same length, we can pair them
            for i in range(min(len(mon_list), len(tue_list))):
                all_data.append({'MON': mon_list[i], 'TUE': tue_list[i]})
    
    return pd.DataFrame(all_data)

def mine_logic():
    print("\n" + "="*70)
    print("  DEEP LOGICAL PATTERN MINING — Tuesday Prediction (MON=74)")
    print("="*70)
    
    df = load_all_data()
    if df.empty:
        print("  ! No data found to mine.")
        return

    # 1. EXACT MATCH LOGIC
    exact_matches = df[df['MON'] == TARGET_MON]
    print(f"\n  [LOGIC 1] Exact Historical Matches (MON was 74)")
    print(f"  ------------------------------------------------")
    if not exact_matches.empty:
        counts = Counter(exact_matches['TUE'])
        for val, count in counts.most_common():
            print(f"    - On {count} occasions, TUE was: {val:02d}")
    else:
        print("    - No exact matches for MON=74 found in filtered data.")

    # 2. DIGIT TENS LOGIC (7X -> ??)
    tens_matches = df[df['MON'] // 10 == TARGET_MON // 10]
    print(f"\n  [LOGIC 2] Tens Digit Logic (MON Tens = 7)")
    print(f"  ------------------------------------------------")
    if not tens_matches.empty:
        tue_tens = Counter(tens_matches['TUE'] // 10)
        tue_units = Counter(tens_matches['TUE'] % 10)
        top_t = tue_tens.most_common(2)
        top_u = tue_units.most_common(2)
        print(f"    - When MON tens is 7, TUE tens is often: {top_t[0][0]} ({top_t[0][1]}x)")
        print(f"    - When MON tens is 7, TUE units is often: {top_u[0][0]} ({top_u[0][1]}x)")
        print(f"    - Logic suggests: {top_t[0][0]}{top_u[0][0]} or {top_t[0][0]}{top_u[1][0]}")

    # 3. DIGIT UNITS LOGIC (X4 -> ??)
    units_matches = df[df['MON'] % 10 == TARGET_MON % 10]
    print(f"\n  [LOGIC 3] Units Digit Logic (MON Units = 4)")
    print(f"  ------------------------------------------------")
    if not units_matches.empty:
        tue_val_counts = Counter(units_matches['TUE'])
        top_v = tue_val_counts.most_common(5)
        print(f"    - When MON units is 4, TUE results are:")
        for v, c in top_v:
            print(f"      - {v:02d} ({c}x)")

    # 4. SUM LOGIC (Total of Digits)
    mon_sum = (TARGET_MON // 10) + (TARGET_MON % 10)
    sum_matches = df[(df['MON'] // 10 + df['MON'] % 10) == mon_sum]
    print(f"\n  [LOGIC 4] Sum Logic (MON Digit Sum = {mon_sum})")
    print(f"  ------------------------------------------------")
    if not sum_matches.empty:
        sum_counts = Counter(sum_matches['TUE'])
        print(f"    - When MON digit sum is {mon_sum}, top TUE outcomes are:")
        for v, c in sum_counts.most_common(3):
            print(f"      - {v:02d} ({c}x)")

    # 5. CYCLE SEARCH (Last 4 weeks)
    print(f"\n  [LOGIC 5] Repeating Sequence Search (Cycle Logic)")
    print(f"  ------------------------------------------------")
    last_5_tue = df['TUE'].tail(5).tolist()
    last_val = last_5_tue[-1]
    # Look for where this value appeared before and what followed it
    indices = [i for i, x in enumerate(df['TUE'].tolist()[:-1]) if x == last_val]
    if indices:
        followers = [df['TUE'].iloc[i+1] for i in indices]
        follow_counts = Counter(followers)
        print(f"    - Last week's TUE was {last_val:02d}.")
        if follow_counts:
            top_f = follow_counts.most_common(2)
            print(f"    - Historically, after TUE={last_val:02d}, the next TUE is often: {top_f[0][0]:02d} ({top_f[0][1]}x)")
    else:
        print("    - No historical cycle match found for last week's result.")

    print("\n" + "="*70)
    print("  CONCLUSION: Multi-Factor Logical Agreement")
    print("="*70)
    print()

if __name__ == "__main__":
    mine_logic()
