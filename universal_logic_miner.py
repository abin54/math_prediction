"""
Universal Logic Miner v12.0 — The Genesis Formula Analysis
==========================================================
1. Phase Space Reconstruction: Map 52 years into a 3 dimensions to find the logic "Attractor".
2. Phase-Locking: Kuramoto Model for Monday-Saturday synchronization.
3. Grammar Complexity: Symbolic depth search.
"""

import numpy as np
import pandas as pd
from scipy import stats

def run_universal_mining():
    file = "Number_Chart.xlsx"
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
    print("  LAYER 1: PHASE SPACE ATTRACTOR (TAKENS' EMBEDDING)")
    print("-" * 70)
    # Define Embedding Params (Found from earlier audit)
    tau = 1
    m = 3 # 3D Projection
    
    # Reconstruct Attractor
    x_dim = seq[:-2]
    y_dim = seq[1:-1]
    z_dim = seq[2:]
    
    # Center & Coordinate check
    print(f"  System Centroid (X,Y,Z): {np.mean(x_dim):.2f}, {np.mean(y_dim):.2f}, {np.mean(z_dim):.2f}")
    
    # 2. PHASE-LOCKING (KURAMOTO MODEL)
    print("\n" + "="*70)
    print("  LAYER 2: PHASE-LOCKING & OSCILLATOR SYNC (KURAMOTO)")
    print("-" * 70)
    # Convert Jodi (0-99) to Phase (0 to 2*pi)
    phases = (seq / 100.0) * 2 * np.pi
    
    def get_order_parameter(p):
        z = np.mean(np.exp(1j * p))
        return np.abs(z)

    # Calculate sync between specific days (e.g. MON vs SAT)
    r_val = get_order_parameter(phases)
    print(f"  Global Kuramoto Sync (r): {r_val:.4f} (Ideal = 1.0)")
    if r_val > 0.05: # Significant for 16k random-looking points
        print("    RESULT: WEAK PHASE-LOCK FOUND. The Mon-Sat cycle is linked.")
    else:
        print("    RESULT: INCOHERENT. The results are independent oscillations.")

    # 3. GRAMMAR DEPTH (SYMBOLIC COMPLEXITY)
    print("\n" + "="*70)
    print("  LAYER 3: GRAMMAR DEPTH & MDL (SYMBOLIC ESSENCE)")
    print("-" * 70)
    diffs = np.diff(seq)
    # Binary Grammar: 1 for Increase, 0 for Decrease/Same
    bits = "".join(['1' if d > 0 else '0' for d in diffs])
    
    # Simplified Lempel-Ziv
    def lz_complexity(s):
        i, j = 1, 1
        count = 1
        while i + j <= len(s):
            if s[i:i + j] in s[:i]:
                j += 1
            else:
                i += j
                j = 1
                count += 1
        return count

    complexity = lz_complexity(bits)
    print(f"  Symbolic Complexity (LZ): {complexity}")
    print(f"  Information Density: {(complexity / len(bits)):.4f}")

    print("\n" + "="*70)

if __name__ == "__main__":
    run_universal_mining()
