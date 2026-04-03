import pandas as pd
import numpy as np
from scipy.stats import entropy
import os

def get_hurst_exponent(ts):
    """Simple R/S Analysis for Hurst Exponent."""
    lags = range(2, 100)
    tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0] * 2.0

def calculate_permutation_entropy(time_series, m=3, delay=1):
    """Calculates Permutation Entropy for Symbol Complexity."""
    n = len(time_series)
    patterns = []
    for i in range(n - (m - 1) * delay):
        pattern = time_series[i:i + m * delay:delay]
        patterns.append(tuple(np.argsort(pattern)))
    
    counts = pd.Series(patterns).value_counts()
    probs = counts / len(patterns)
    return -np.sum(probs * np.log2(probs))

def run_physics_audit():
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
    print("  MODEL v12.0: THE PHYSICS & INFORMATION AUDIT (52 YEARS)")
    print("-" * 70)
    
    # 1. Hurst Exponent (Chaos vs. Persistence)
    h = get_hurst_exponent(seq)
    print(f"  [Fractal] Hurst Exponent (H): {h:.4f}")
    if h > 0.5:
        print("    -> PERSISTENT: Day 1 logic survives 52 years later.")
    else:
        print("    -> MEAN-REVERTING: The system corrects itself towards a baseline.")
        
    # 2. Permutation Entropy (Predictability)
    pe = calculate_permutation_entropy(seq)
    print(f"  [Entropy] Permutation Entropy: {pe:.4f}")
    
    # 3. Phase Space (Takens' Delay Recommendation)
    # Finding Tau using Autocorrelation drop-off
    acf = np.correlate(seq - np.mean(seq), seq - np.mean(seq), mode='full')[n-1:]
    tau = np.where(acf < acf[0] * (1 - 1/np.exp(1)))[0][0]
    print(f"  [Phase Space] Optimal Time Delay (Tau): {tau}")
    
    # 4. Symbol Strings (U/D/S Logic)
    diffs = np.diff(seq)
    symbols = ['U' if d > 0 else ('D' if d < 0 else 'S') for d in diffs]
    sym_counts = pd.Series(symbols).value_counts()
    print(f"  [Symbolic] Grammar Distribution: U={sym_counts.get('U',0)}, D={sym_counts.get('D',0)}, S={sym_counts.get('S',0)}")
    
    # 5. Transfer Entropy Proxy (1970s block -> 2020s block)
    block_70s = seq[:300]
    block_20s = seq[-300:]
    # Check if distribution changed significantly
    ks_stat, p_val = stats.ks_2samp(block_70s, block_20s)
    print(f"  [Causal] KS Stability Test (1970s vs 2020s): p={p_val:.4f}")
    if p_val > 0.05:
        print("    -> CAUSAL ANCHOR: The 1970s distribution is nearly identical to the 2020s.")
    else:
        print("    -> REGIME SHIFT: The source code has mutated over 5 decades.")

    print("\n" + "="*70)

if __name__ == "__main__":
    from scipy import stats
    run_physics_audit()
