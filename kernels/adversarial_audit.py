import pandas as pd
import numpy as np
from collections import Counter
import os

# --- CONTEXT ---
YESTERDAY = 16
OPEN_VAL = 1
UNIT_VAL = 6
TARGET_DAY = "FRI"

def load_data():
    if os.path.exists("Number_Chart.xlsx"):
        df = pd.read_excel("Number_Chart.xlsx", sheet_name="Sheet1")
        return df
    return None

def run_adversarial_audit():
    print("\n" + "="*80)
    print("  ADVERSARIAL AUDIT: CRITICAL FAILURE ANALYSIS")
    print("="*80)
    print(f"  Current Hypothesis: [Symmetry Shift] -> Predicted Open: 3/8")
    print(f"  Audit Goal: Identify 'Black Swan' patterns that could break the streak.")
    
    df = load_data()
    if df is None: return
    
    fri_vals = df["FRI Jodi Num"].dropna().astype(int).tolist()
    
    # 1. COUNTER-TREND: Open Repetition (The 'Echo' failure)
    # What if the Open 1 just repeats instead of shifting?
    repeats_1 = len([v for v in fri_vals if v // 10 == 1])
    print(f"\n  [Vulnerability 1] Open Repetition (1 -> 1):")
    print(f"    - Historical probability of 1-Open repeating on Friday: {len([v for v in fri_vals if v//10 == 1])/len(fri_vals):.1%}")
    
    # 2. OVERDUE REVENGE (The 'Outlier' failure)
    # Which Open has not appeared for the longest time?
    last_seen_open = {}
    for i, v in enumerate(fri_vals):
        last_seen_open[v // 10] = i
    current_idx = len(fri_vals) - 1
    overdue_open = sorted({o: current_idx - idx for o, idx in last_seen_open.items()}.items(), key=lambda x: -x[1])
    print(f"\n  [Vulnerability 2] Overdue 'Outlier' Revenge:")
    print(f"    - Longest Overdue Friday Open: {overdue_open[0][0]} (Not seen for {overdue_open[0][1]} weeks)")
    
    # 3. UNIT PARITY BREAK (The 'Crossing' failure)
    # This week has been Odd-Even-Odd-Even. 
    # Mon(7) Tue(0) Wed(1) Thu(1) -> Wait, Wed/Thu were both Odd.
    # Pattern: 7 - 0 - 1 - 1.
    # What if the Parity shifts to a 'Double Even' today?
    print(f"\n  [Vulnerability 3] Parity Sequence Conflict:")
    print(f"    - Prediction 3 is ODD. If the sequence breaks to EVEN, target: 2 or 6.")

    print("\n" + "="*80)
    print("  ADVERSARIAL RECOMMENDATION: SAFETY BUFFER")
    print("="*80)
    print(f"  If the 'Symmetry Trick' (3/8) fails, the most likely 'Black Swan' is:")
    print(f"  >>> SAFETY OPEN: {overdue_open[0][0]} (Overdue) or 1 (Repetition)")
    print("=" * 80)

if __name__ == "__main__":
    run_adversarial_audit()
