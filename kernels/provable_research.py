import pandas as pd
import numpy as np
import os
from scipy.optimize import curve_fit

def run_provable_research():
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
    
    # 1. S5-Style Functional Basis Search (Continuous Flow)
    def basis_func(t, a, b, c, d):
        return a * np.sin(b * t + c) + d
    
    t = np.arange(n)
    try:
        popt, _ = curve_fit(basis_func, t, seq, p0=[20, 2*np.pi/9, 0, 50])
        print("\n" + "="*70)
        print("  MODEL v16.0: S5 BASIS & SYMBOLIC LOGIC AUDIT (52 YEARS)")
        print("-" * 70)
        print(f"  [S5 Basis] Optimal Curve: f(t) = {popt[0]:.2f}*sin({popt[1]:.4f}*t + {popt[2]:.2f}) + {popt[3]:.2f}")
    except:
        print("\n  [S5 Basis] Failed to fit global curve.")
        
    # 2. Symbolic Logic Prover (Unbroken Laws since 1972)
    # Checking for Modulo Invariants: Result % M = Constant?
    print(f"\n  [Symbolic] Searching for UNBROKEN LAWS across {n} days:")
    for m in range(2, 11):
        first_mod = int(seq[0]) % m
        broken = False
        for i, v in enumerate(seq):
            if int(v) % m != first_mod:
                broken = True
                break
        if not broken:
            print(f"    -> LAW FOUND: Every single result in 52 years satisfies X mod {m} = {first_mod}")
        else:
            print(f"    -> X mod {m} rule broken on Day {i}")
            
    # 3. Regime Shift Detection (Decadal Evolution)
    dec1_mean = np.mean(seq[:1000])
    dec5_mean = np.mean(seq[-1000:])
    print(f"\n  [Regime] Decadal Mean Evolution: {dec1_mean:.2f} (1970s) -> {dec5_mean:.2f} (2020s)")

    print("\n" + "="*70)

if __name__ == "__main__":
    run_provable_research()
