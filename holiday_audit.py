import pandas as pd
import numpy as np
import os

def run_holiday_audit():
    file = "Number_Chart.xlsx"
    if not os.path.exists(file):
        print("File not found.")
        return
        
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    holidays_found = 0
    days_cols = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    
    holiday_map = []
    
    for idx, row in df.iterrows():
        week_stats = {"idx": idx, "holidays": []}
        for d in days_cols:
            v = str(row[f"{d} Jodi Num"]).strip()
            if "★" in v or v == "" or v == "nan" or v == " " or v == "None":
                holidays_found += 1
                week_stats["holidays"].append(d)
        if week_stats["holidays"]:
            holiday_map.append(week_stats)
            
    print("\n" + "="*70)
    print("  MODEL v16.1: HOLIDAY-AWARE TEMPORAL AUDIT (52 YEARS)")
    print("-" * 70)
    print(f"  Total Historical Holidays (★) Detected: {holidays_found}")
    print(f"  Holiday Frequency: {(holidays_found / (len(df) * 6)) * 100:.2f}% of total days")
    
    if holiday_map:
        print("\n  Sample Holiday Gaps (Recent):")
        for h in holiday_map[-5:]:
            print(f"    - Year-Idx {h['idx']}, Days: {', '.join(h['holidays'])}")
            
    print("\n  [CORRECTION STRATEGY]:")
    print("    -> Skip Holidays in 'Sequence Flow' to prevent 9-Day cycle drift.")
    print("    -> Maintain 'Day-of-Week' identity using a Masked Temporal Index.")

    print("\n" + "="*70)

if __name__ == "__main__":
    run_holiday_audit()
