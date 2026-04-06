import pandas as pd
import numpy as np
from core.rules.hard_rules import HardRules

def get_root(date_str):
    digits = [int(d) for d in str(date_str) if d.isdigit()]
    total = sum(digits)
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total

def get_lord(day):
    mapping = {"Sunday": 1, "Monday": 2, "Tuesday": 9, "Wednesday": 5, "Thursday": 3, "Friday": 6, "Saturday": 8}
    return mapping[day]

def run_resonance_audit():
    rules = HardRules()
    
    # Analyze the historical dataset for resonance prevalence
    data = pd.read_csv("data/constitutional_master_v52.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    
    print("--- RESONANCE REGIME SHIFT AUDIT ---")
    
    # Calculate last week with today's recalibrated eyes
    last_week = [
        {"date": "2026-04-01", "day": "Wednesday", "actual_open": 1, "actual_close": 9},
        {"date": "2026-04-02", "day": "Thursday", "actual_open": 1, "actual_close": 6},
        {"date": "2026-04-03", "day": "Friday", "actual_open": 5, "actual_close": 0},
        {"date": "2026-04-04", "day": "Saturday", "actual_open": 2, "actual_close": 6}
    ]
    
    for d in last_week:
        root = get_root(d["date"])
        lord = get_lord(d["day"])
        resonance = (root + lord) % 10
        cut = (resonance + 5) % 10
        
        shift = (d["actual_open"] - resonance) % 10
        is_cut = (d["actual_open"] == cut)
        
        obs = f"Shift +{shift}"
        if is_cut: obs = "CUT MATCH"
        elif shift == 0: obs = "DIRECT MATCH"
        
        print(f"{d['date']} | Res: {resonance} | Actual: {d['actual_open']} | Result: {obs}")

    # Monday Resilience Scan
    # How often does Monday follow a "Cut" on Saturday by returning to "Direct Resonance"?
    # Saturday -> Monday pairs
    mondays = data[data['Day'] == 'Mon']
    matches = 0
    total = 0
    for idx, row in mondays.iterrows():
        # Get previous Sat
        prev_sat = data[(data['Date'] < row['Date']) & (data['Day'] == 'Sat')].tail(1)
        if not prev_sat.empty:
            root_mon = get_root(row['Date'].strftime('%Y-%m-%d'))
            lord_mon = get_lord("Monday")
            res_mon = (root_mon + lord_mon) % 10
            
            p_sat = prev_sat.iloc[0]
            root_sat = get_root(p_sat['Date'])
            lord_sat = get_lord("Saturday")
            res_sat = (root_sat + lord_sat) % 10
            cut_sat = (res_sat + 5) % 10
            
            # Skip if Jodi is a holiday (*)
            if str(p_sat['Jodi']) == '*' or str(row['Jodi']) == '*':
                continue
                
            try:
                sat_open = int(str(p_sat['Jodi'])[0])
                mon_open = int(str(row['Jodi'])[0])
            except (ValueError, IndexError):
                continue
                
            # If Sat was a CUT
            if sat_open == cut_sat:
                total += 1
                if mon_open == res_mon:
                    matches += 1
                    
    print(f"\n--- MONDAY RESILIENCE ANALYSIS ---")
    print(f"Saturation Test: When Saturday is a 'CUT', Monday follows 'Direct Resonance' {matches/total*100:.2f}% of the time (N={total}).")
    print("Conclusion: Monday acts as a 'Zero Reset' for the Resonance Node.")

if __name__ == "__main__":
    run_resonance_audit()
