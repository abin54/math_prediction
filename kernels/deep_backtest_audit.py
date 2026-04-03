import pandas as pd
import numpy as np
import os, json
from swarm_predictor import run_swarm

def perform_backtest(days_to_test=10):
    df = pd.read_excel("Number_Chart.xlsx", sheet_name="Numeric Analysis")
    # Flatten results into a date-ordered sequence
    # This is tricky because the chart is day-wise. 
    # Let's just test the last 5 of each day.
    
    results = {}
    for day in ["MON", "TUE", "WED", "THU", "FRI", "SAT"]:
        col = f"{day} Jodi Num"
        if col in df.columns:
            vals = df[col].dropna().astype(int).tolist()
            results[day] = vals

    print("\n" + "="*80)
    print(f"  DEEP FORENSIC BACKTEST — Last {days_to_test} Weeks")
    print("="*80)

    # We'll test the last few 'Transition' points.
    # For Sunday/Monday, TUE/WED etc.
    # We'll focus on the most recent 10 results in the 'Monday' column as a proxy for 'weeks'.
    
    success_count = 0
    total_count = 0
    
    # We want to test the very last 5 weeks specifically.
    for i in range(-days_to_test, 0):
        # Target: Monday
        try:
            target_val = results["MON"][i]
            prev_val = results["SAT"][i-1] # Saturday of previous week
            print(f"\n[TESTING MON] Previous SAT={prev_val:02d} -> Actual MON={target_val:02d}")
            
            # Silence swarm output for clean report
            import contextlib, io
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                preds = run_swarm(target_day="MON", yesterday_day="SAT", yesterday_jodi=prev_val)
            
            top4 = [p[0] for p in preds[:4]]
            if target_val in top4:
                print(f"  >>> SUCCESS! Predicted {target_val:02d} in Top 4: {top4}")
                success_count += 1
            else:
                # NEW: Analyze WHY it failed
                mirror_of_prev = {0:5,1:6,2:7,3:8,4:9,5:0,6:1,7:2,8:3,9:4}
                p_t, p_u = prev_val // 10, prev_val % 10
                is_mirror = (target_val == mirror_of_prev[p_t]*10 + mirror_of_prev[p_u])
                is_cut = (target_val // 10 == mirror_of_prev[p_t] or target_val % 10 == mirror_of_prev[p_u])
                
                print(f"  [FAILURE] Top 4: {top4} | Actual: {target_val:02d}")
                if is_mirror: print("    Reason: Missed FULL MIRROR pattern")
                if is_cut: print("    Reason: Missed CUT DIGIT pattern")
            
            total_count += 1
        except Exception as e:
            print(f"  [ERROR] Skipping: {e}")

    print("\n" + "="*80)
    print(f"  FINAL SCORE: {success_count}/{total_count} ({success_count/total_count:.1%})")
    print("="*80)

if __name__ == "__main__":
    perform_backtest(5)
