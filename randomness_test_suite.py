import pandas as pd
import numpy as np
from scipy import stats
from collections import Counter

def get_total(v):
    try:
        v = int(pd.to_numeric(v, errors='coerce'))
        return (v // 10 + v % 10) % 10
    except:
        return -1

def run_tests():
    file = "Number_Chart.xlsx"
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    
    sequence = []
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    for idx, row in df.iterrows():
        for d in days:
            v = row[f"{d} Jodi Num"]
            if not pd.isna(v):
                sequence.append(int(v))
    
    seq = np.array(sequence)
    n = len(seq)
    
    print("\n" + "="*70)
    print("  STOCHASTIC vs. DETERMINISTIC AUDIT (54-YEAR DATASET)")
    print("-" * 70)
    print(f"  Total Samples: {n}")
    
    # 1. Chi-Squared Uniformity Test
    observed = Counter(sequence)
    obs_counts = [observed.get(i, 0) for i in range(100)]
    expected_counts = [n / 100] * 100
    chi2, p_val = stats.chisquare(obs_counts, expected_counts)
    
    # 2. Wald-Wolfowitz Runs Test
    # (Testing for randomness in high/low sequence)
    median_val = np.median(seq)
    binary_seq = np.array([1 if x > median_val else 0 for x in seq])
    runs = np.where(np.diff(binary_seq) != 0)[0].size + 1
    n1 = np.sum(binary_seq == 1)
    n2 = np.sum(binary_seq == 0)
    exp_runs = ((2.0 * n1 * n2) / (n1 + n2)) + 1
    var_runs = (2.0 * n1 * n2 * (2.0 * n1 * n2 - n1 - n2)) / \
               (((n1 + n2)**2) * (n1 + n2 - 1))
    z = (runs - exp_runs) / np.sqrt(var_runs)
    p_runs = stats.norm.sf(abs(z)) * 2 # Two-sided p-value
    
    # 3. Simple Lag-1 Autocorrelation (Numpy version)
    lag1 = np.corrcoef(seq[:-1], seq[1:])[0, 1]

    # 4. Step-3 Logic Enrichment
    tots = [get_total(v) for v in sequence]
    step3_hits = 0
    for i in range(len(tots)-1):
        if (tots[i] + 3) % 10 == tots[i+1]:
            step3_hits += 1
    expected_step3 = (n - 1) * 0.1

    print("\n  LOGICAL SUMMARY:")
    print("-" * 70)
    
    # Report Uniformity
    print(f"  [Uniformity]  p: {p_val:.4f}")
    if p_val < 0.05:
        print("    -> DETERMINISTIC: Significant bias in number distribution (Loaded numbers).")
    else:
        print("    -> STOCHASTIC: Data is uniformly distributed like a clear random wheel.")
        
    # Report Runs
    print(f"  [Randomness]  p: {p_runs:.4f} (Runs Test)")
    if p_runs < 0.05:
        print("    -> DETERMINISTIC: Patterns found in High/Low transitions (Predictable shifts).")
    else:
        print("    -> STOCHASTIC: High/Low transitions are as random as a coin flip.")

    # Report Memory
    print(f"  [Memory]      Lag-1 Corr: {lag1:.4f}")
    if abs(lag1) > 0.05:
        print("    -> DETERMINISTIC: Today's number has 'Memory' of yesterday.")
    else:
        print("    -> STOCHASTIC: Numbers are independent (No memory).")

    # Report Trick Logic
    print(f"  [Trick Boost] Step-3 logic hits {step3_hits/expected_step3 - 1:+.1%} vs. pure chance.")
    if step3_hits > expected_step3 * 1.05:
        print("    -> DETERMINISTIC: Trick Logic significantly outperforms random noise.")
    else:
        print("    -> STOCHASTIC: Trick Logic is within the bounds of luck.")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    run_tests()
