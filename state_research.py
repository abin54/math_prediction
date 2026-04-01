import pandas as pd
import numpy as np
import os

def run_state_research():
    file = "Number_Chart.xlsx"
    if not os.path.exists(file):
        print("File not found.")
        return
        
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    sequence = []
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    for idx, row in df.iterrows():
        for d in days:
            v = row[f"{d} Jodi Num"]
            if not pd.isna(v): sequence.append(float(v))
            
    seq = np.array(sequence)
    n = len(seq)
    
    print("\n" + "="*70)
    print("  MODEL v15.0: DILATED CORRELATION & STATE SPACE AUDIT (52 YEARS)")
    print("-" * 70)
    print(f"  Total Historical Sequence points: {n}")
    
    # 1. DILATED CORRELATION (WaveNet style)
    # Checking for "Scale-Invariant" logic at different powers of 10
    lags = [1, 10, 100, 1000, 10000]
    for d in lags:
        if n > d:
            corr = np.corrcoef(seq[:-d], seq[d:])[0, 1]
            print(f"    Lag {d:5d} Correlation: {corr:.4f}")
            
    # 2. MAMBA SSM HIDDEN STATE SIMULATION
    # h_t = A * h_t-1 + B * x_t (Simplified)
    # We use a long-memory coefficient (kappa)
    kappa = 0.999 # 99.9% persistence to reach back to 1970s
    state = 0
    history_states = []
    for v in seq:
        state = kappa * state + (1 - kappa) * v
        history_states.append(state)
        
    final_h = state
    print(f"\n  [Mamba] 52-Year Hidden State (h_final): {final_h:.2f}")
    
    # 3. LEAST ACTION PRINCIPLE (Lagrangian Logic)
    # Finding the path that has the lowest volatility relative to the state
    residuals = seq - history_states
    action = np.mean(np.square(residuals))
    print(f"  [Physics] Global Action (Mean Variance): {action:.2f}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    run_state_research()
