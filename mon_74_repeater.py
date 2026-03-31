"""
Monday 74 Follower Miner — Exact Tuesday repetitions
=====================================================
Finds every instance of Monday=74 and shows exactly what happened on Tuesday.
Identifies any repeating Tuesday results (repetitions).
"""

import pandas as pd
import os
from collections import Counter

# CONFIG
EXCEL_FILE_1 = "Number_Chart.xlsx"
EXCEL_FILE_2 = "Kalyan_Panel_Chart_Dataset.xlsx"
TARGET_MON = 74

def get_pairs():
    pairs = []
    
    # Source 1: Number_Chart.xlsx (Wide format)
    if os.path.exists(EXCEL_FILE_1):
        try:
            df = pd.read_excel(EXCEL_FILE_1, sheet_name="Numeric Analysis", header=0)
            if "MON Jodi Num" in df.columns and "TUE Jodi Num" in df.columns:
                m = pd.to_numeric(df["MON Jodi Num"], errors="coerce")
                t = pd.to_numeric(df["TUE Jodi Num"], errors="coerce")
                valid = pd.concat([m, t], axis=1).dropna().astype(int)
                for _, row in valid.iterrows():
                    pairs.append({'m': row.iloc[0], 't': row.iloc[1], 'src': 'Number_Chart'})
        except Exception as e:
            print(f"Error reading {EXCEL_FILE_1}: {e}")

    # Source 2: Kalyan_Panel_Chart_Dataset.xlsx (Long format)
    if os.path.exists(EXCEL_FILE_2):
        try:
            df2 = pd.read_excel(EXCEL_FILE_2)
            cols = {c.strip().lower(): c for c in df2.columns}
            if 'day' in cols and 'jodi' in cols:
                df2['day_clean'] = df2[cols['day']].astype(str).str.strip().str.upper()
                df2['jodi_num'] = pd.to_numeric(df2[cols['jodi']], errors="coerce")
                
                # We need to find Monday, then the very next Tuesday in the log
                # We'll iterate through the rows
                last_mon_jodi = None
                for _, row in df2.iterrows():
                    day = str(row['day_clean'])
                    jodi = row['jodi_num']
                    if pd.isna(jodi): continue
                    
                    if day.startswith('MON'):
                        last_mon_jodi = int(jodi)
                    elif day.startswith('TUE') and last_mon_jodi is not None:
                        pairs.append({'m': last_mon_jodi, 't': int(jodi), 'src': 'Kalyan_Dataset'})
                        last_mon_jodi = None # reset
                    elif day.startswith('SAT') or day.startswith('FRI'):
                        last_mon_jodi = None # reset if we skip mid-week
        except Exception as e:
            print(f"Error reading {EXCEL_FILE_2}: {e}")
            
    return pairs

def analyze_74():
    pairs = get_pairs()
    matches = [p['t'] for p in pairs if p['m'] == TARGET_MON]
    
    print("\n" + "="*70)
    print(f"  EXACT REPETITION ANALYSIS — When Monday was {TARGET_MON}")
    print("="*70)
    print(f"  Total historical instances of MON={TARGET_MON} found: {len(matches)}")
    print("-" * 70)
    
    if not matches:
        print(f"  No instances of Monday={TARGET_MON} were found in the datasets.")
        return

    # Count repetitions
    counts = Counter(matches)
    reps = {val: cnt for val, cnt in counts.items() if cnt > 1}
    singletons = {val: cnt for val, cnt in counts.items() if cnt == 1}

    print("\n  [REPEATING TUESDAYS] — Numbers that appeared more than once:")
    if reps:
        for val, cnt in sorted(reps.items(), key=lambda x: -x[1]):
            print(f"    - Jodi {val:02d} appeared {cnt} times")
    else:
        print("    - None found.")

    print("\n  [SINGLETON TUESDAYS] — Numbers that appeared only once:")
    if singletons:
        s_list = sorted(singletons.keys())
        # Print in groups of 5
        for i in range(0, len(s_list), 5):
            print("    - " + ", ".join(f"{v:02d}" for v in s_list[i:i+5]))

    print("\n" + "="*70)
    print("  LOGICAL CONCLUSION")
    print("="*70)
    if reps:
        best_rep = max(reps.items(), key=lambda x: x[1])[0]
        print(f"    There IS a repetition pattern. The number {best_rep:02d} has the")
        print(f"    highest repetition rate (Appeared {reps[best_rep]}x after 74).")
    else:
        print("    No direct number repetition found. The system likely follows")
        print("    digit-based shifts rather than exact number repeats.")
    print("="*70)
    print()

if __name__ == "__main__":
    analyze_74()
