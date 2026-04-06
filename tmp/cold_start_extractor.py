import pandas as pd
import json
import os

def get_root(date_str):
    t = sum([int(d) for d in str(date_str).replace('-', '').replace('/', '') if d.isdigit()])
    while t > 9:
        t = sum([int(d) for d in str(t)])
    return t

def run_cold_start_extraction():
    data = pd.read_csv("data/constitutional_master_v52.csv")
    lord_map = {'Sun': 1, 'Mon': 2, 'Tue': 9, 'Wed': 5, 'Thu': 3, 'Fri': 6, 'Sat': 8}
    
    results = []
    
    print("--- [PHASE 1: COLD START SFT EXTRACTION] ---")
    
    for _, row in data.iterrows():
        try:
            j = str(row['Jodi']).strip()
            if j in ['*', 'XX', 'NaN']:
                continue
                
            op = int(j[0])
            cl = int(j[1])
            rt = get_root(row['Date'])
            ld = lord_map.get(row['Day'], 0)
            
            # Condition for "Golden Proof" (Triple-Resonance)
            if op == rt == ld:
                results.append({
                    "date": str(row['Date']),
                    "jodi": j,
                    "logic": "Triple-Resonance (Root=Lord=Open)",
                    "derivation": f"Root({rt}) + Lord({ld}) convergence on Open({op})"
                })
        except:
            continue
            
    # Save to core/training/
    os.makedirs("core/training", exist_ok=True)
    with open("core/training/golden_start_dataset.json", "w") as f:
        json.dump(results[:500], f, indent=4)
        
    print(f"Extracted {len(results)} Golden Proofs for SFT Priming.")
    print("Successfully saved to core/training/golden_start_dataset.json")

if __name__ == "__main__":
    run_cold_start_extraction()
