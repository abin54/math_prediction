import pandas as pd
import numpy as np

def get_root(dt):
    t = sum([int(d) for d in dt.strftime('%Y%m%d') if d.isdigit()])
    while t > 9:
        t = sum([int(d) for d in str(t)])
    return t

def run_triple2_historical_audit():
    data = pd.read_csv("data/constitutional_master_v52.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    lord_map = {'Sun':1, 'Mon':2, 'Tue':9, 'Wed':5, 'Thu':3, 'Fri':6, 'Sat':8}
    
    total = 0
    wins = 0
    failing_dates = []
    
    print("--- [TRIPLE-2 MONDAY HISTORICAL AUDIT: 1972-2026] ---")
    
    for idx, row in data.iterrows():
        try:
            j = str(row['Jodi']).strip()
            if j in ['*', 'XX', 'NaN']:
                continue
                
            op = int(j[0])
            dt = row['Date']
            rt = get_root(dt)
            ld = lord_map.get(row['Day'], 0)
            
            # Today's Logic Condition: Monday (Day Lord 2) + Date Root 2
            if row['Day'] == 'Mon' and rt == 2 and ld == 2:
                total += 1
                if op == 2:
                    wins += 1
                else:
                    failing_dates.append({
                        "date": dt.strftime('%Y-%m-%d'),
                        "actual": op,
                        "resonance": rt
                    })
        except:
            continue
            
    if total == 0:
        print("No Triple-2 Mondays found in history.")
        return

    win_rate = (wins / total) * 100
    print(f"Total Triple-2 Mondays: {total}")
    print(f"Logic Wins (Open 2): {wins}")
    print(f"Logic Fails: {total - wins}")
    print(f"Historical Win Rate: {win_rate:.2f}%")
    
    if failing_dates:
        print("\n--- FAILURE LOG: THE GHOST NODES ---")
        for f in failing_dates[:5]:
            print(f"Date: {f['date']} | Logic: 2 | Actual: {f['actual']} (Anomaly)")

if __name__ == "__main__":
    run_triple2_historical_audit()
