import pandas as pd
import numpy as np

def get_root(dt):
    t = sum([int(d) for d in dt.strftime('%Y%m%d') if d.isdigit()])
    while t > 9:
        t = sum([int(d) for d in str(t)])
    return t

def run_outlier_logic_audit():
    data = pd.read_csv("data/constitutional_master_v52.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    lord_map = {'Sun':1, 'Mon':2, 'Tue':9, 'Wed':5, 'Thu':3, 'Fri':6, 'Sat':8}
    
    # Target Triple-2 Monday Metadata
    target_rt = 2
    target_ld = 2
    excluded_ops = [2, 7]
    
    outlier_hits = []
    
    print("--- [SOVEREIGN OUTLIER AUDIT: NON-2 / NON-7 MONDAYS] ---")
    
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
            if row['Day'] == 'Mon' and rt == target_rt and ld == target_ld:
                if op not in excluded_ops:
                    outlier_hits.append({
                        "date": dt.strftime('%Y-%m-%d'),
                        "jodi": j,
                        "open": op,
                        "close": int(j[1])
                    })
        except:
            continue
            
    if not outlier_hits:
        print("No outlier Triple-2 Mondays found in history (outside 2 and 7).")
        return

    df_outliers = pd.DataFrame(outlier_hits)
    
    # Aggregate by Open
    open_ranking = df_outliers['open'].value_counts()
    print("\n--- ALTERNATIVE OPEN RANKING (When 2/7 are Bypassed) ---")
    print(open_ranking)
    
    # Aggregate by Jodi
    jodi_ranking = df_outliers['jodi'].value_counts()
    print("\n--- ALTERNATIVE JODI RANKING (Top 5 Survivors) ---")
    print(jodi_ranking.head(5))
    
    # Logic Cluster Audit
    sum_node_wins = len(df_outliers[df_outliers['open'] == 4])
    silence_node_wins = len(df_outliers[df_outliers['open'].isin([0, 5])])
    step_node_wins = len(df_outliers[df_outliers['open'].isin([1, 3])])
    
    print("\n--- LOGIC CLUSTER WIN RATES ---")
    print(f"Cluster 4 (Sum Resonance): {sum_node_wins} Wins")
    print(f"Cluster 0/5 (Silence/Reset): {silence_node_wins} Wins")
    print(f"Cluster 1/3 (Step Shift): {step_node_wins} Wins")

if __name__ == "__main__":
    run_outlier_logic_audit()
