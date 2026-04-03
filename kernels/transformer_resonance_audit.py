import pandas as pd
import numpy as np
from scipy.signal import find_peaks

def find_resonance_heads():
    file = "Number_Chart.xlsx"
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    sequence = []
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    for idx, row in df.iterrows():
        for d in days:
            v = row[f"{d} Jodi Num"]
            if not pd.isna(v): sequence.append(float(v))
    
    seq = np.array(sequence)
    
    # Calculate ACF to find "Resonance" points for Transformer Heads
    def get_acf(ts, nlags):
        n = len(ts)
        mean = np.mean(ts)
        var = np.var(ts)
        acf = []
        for lag in range(nlags):
            cov = np.sum((ts[:n-lag] - mean) * (ts[lag:] - mean)) / n
            acf.append(cov / var)
        return np.array(acf)

    # Search for long-term resonance (up to 1 year / 300 days)
    acf_vals = get_acf(seq, 365)
    peaks, _ = find_peaks(acf_vals, distance=5, height=0.01)
    
    print("\n" + "="*70)
    print("  TRANSFORMER RESONANCE AUDIT (ATTENTION HEAD DESIGN)")
    print("-" * 70)
    print(f"  Searching for 'Global Logic' peaks across 52 years...")
    
    sorted_peaks = peaks[np.argsort(acf_vals[peaks])][::-1]
    
    for i, p in enumerate(sorted_peaks[:8]):
        print(f"    Head {i+1}: Resonance at {p} days (Corr: {acf_vals[p]:.4f})")
        
    print("\n  Summary for Transformer Configuration:")
    print(f"    - Short-term Heads: {sorted_peaks[0]} days (Week/Cycle)")
    print(f"    - Mid-term Heads: {sorted_peaks[1]} days (Month/Season)")
    print(f"    - Global Logic Head: {sorted_peaks[2]} days (Annual Correlation)")
    print("="*70)

if __name__ == "__main__":
    find_resonance_heads()
