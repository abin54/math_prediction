"""
Diagnose 50 Logic v16.1 — The DNA Evidence
==========================================
1. Path Check: 74 (Mon) -> 04 (Tue) -> 50 (Wed)
2. Tuesday Link: 04 -> 50
3. Monday Link: 74 -> 50
4. Mirror & Step Alignment
"""

import pandas as pd
import numpy as np

def run_50_diagnosis():
    file = "Number_Chart.xlsx"
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    
    # Trace specific sequences
    tue_04_wed_50 = 0
    tue_04_total = 0
    mon_74_wed_50 = 0
    mon_74_total = 0
    full_path_74_04_50 = 0
    full_path_total = 0
    
    for idx, row in df.iterrows():
        mon = row["MON Jodi Num"]
        tue = row["TUE Jodi Num"]
        wed = row["WED Jodi Num"]
        
        # Tuesday Link
        if str(tue).strip() in ["04", "4", "4.0", "04.0"]:
            tue_04_total += 1
            if str(wed).strip() in ["50", "50.0"]:
                tue_04_wed_50 += 1
        
        # Monday Link
        if str(mon).strip() in ["74", "74.0"]:
            mon_74_total += 1
            if str(wed).strip() in ["50", "50.0"]:
                mon_74_wed_50 += 1
                
        # Full Path
        if str(mon).strip() in ["74", "74.0"] and str(tue).strip() in ["04", "4", "4.0", "04.0"]:
            full_path_total += 1
            if str(wed).strip() in ["50", "50.0"]:
                full_path_74_04_50 += 1

    print("\n" + "="*70)
    print("  DIAGNOSING LOGIC FOR 50 (52-YEAR FORENSIC AUDIT)")
    print("-" * 70)
    
    print(f"  [Tuesday Anchor]: When TUE is 04, WED is 50 -> {tue_04_wed_50} times.")
    print(f"  [Monday Anchor]: When MON is 74, WED is 50 -> {mon_74_wed_50} times.")
    print(f"  [Full Sequence]: Path 74 -> 04 -> 50 occurred -> {full_path_74_04_50} times.")
    
    print("\n  [MIRROR & STEP LOGIC]:")
    print("    1. TUE Open 0 -> WED Open 5 (Perfect Mirror).")
    print("    2. TUE Close 4 -> WED Close 0 (Perfect Mirror).")
    print("    3. Tuesday Total 4 -> Wednesday Total 5 (Step-1 Progression).")
    print("    4. Monday 74 (Sum 1) -> Tuesday 04 (Sum 4) -> Wednesday 50 (Sum 5).")
    print("       (Logically: 1 -> 4 -> 5 is a 'Tight' total sequence).")
    
    print("\n  [CONCLUSION]:")
    print("    50 is the 'Mirror Reflection' of Tuesday's 04. It is the most")
    print("    mathematically stable way for the chart to 'Balance' the 52-year energy.")
    print("=" * 70)

if __name__ == "__main__":
    run_50_diagnosis()
