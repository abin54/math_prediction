import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import os

def get_total(v):
    try:
        v = int(pd.to_numeric(v, errors='coerce'))
        return (v // 10 + v % 10) % 10
    except:
        return -1

def analyze_lags_and_entropy():
    file = "Number_Chart.xlsx"
    if not os.path.exists(file):
        print("File not found.")
        return
        
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    
    # Flatten sequence for lag analysis
    sequence = []
    dates = []
    days_map = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    
    for idx, row in df.iterrows():
        for d in days_map:
            v = row[f"{d} Jodi Num"]
            if not pd.isna(v):
                sequence.append(float(v))
                dates.append(row["Date Range"])
                
    seq = np.array(sequence)
    n = len(seq)
    
    print("\n" + "="*70)
    print("  1. LAG ANALYSIS & AUTOCORRELATION STUDY")
    print("-" * 70)
    
    lags = [1, 6, 30]
    for lag in lags:
        if n > lag:
            corr, p = pearsonr(seq[:-lag], seq[lag:])
            print(f"    Lag {lag:2} (Day N vs N+{lag}): Correlation={corr:+.4f} | p={p:.4f}")
    
    # 2. First Day Hypothesis
    print("\n" + "="*70)
    print("  2. FIRST DAY HYPOTHESIS (Monthly/Yearly)")
    print("-" * 70)
    
    # Extract Month/Year
    import re
    def parse_dm(s):
        try:
            m = re.search(r'(\d{2})/(\d{2})/(\d{2,4})', str(s))
            return int(m.group(1)), int(m.group(2)), int(m.group(3))
        except:
            return 0, 0, 0

    first_days_month = []
    subsequent_avg_month = []
    
    # We'll use the Monday of each week as a proxy for 'First Day' checks if exact dates aren't aligned
    # But better: find rows where day is 01
    df['DayNum'] = df['Date Range'].apply(lambda x: parse_dm(x)[0])
    df['Month'] = df['Date Range'].apply(lambda x: parse_dm(x)[1])
    
    # Correlation between First Monday of month and the rest of the month
    # To keep it simple: check if MON predicts SAT in the same week
    mon_vals = df['MON Jodi Num'].dropna()
    sat_vals = df['SAT Jodi Num'].dropna()
    common_idx = mon_vals.index.intersection(sat_vals.index)
    if not common_idx.empty:
        corr_ms, p_ms = pearsonr(mon_vals.loc[common_idx], sat_vals.loc[common_idx])
        print(f"    MON vs SAT (Same Week) Correlation: {corr_ms:+.4f} (p={p_ms:.4f})")

    # 3. Entropy Shifts (Rolling Shannon Entropy)
    print("\n" + "="*70)
    print("  3. ENTROPY SHIFTS (Predictability Audit)")
    print("-" * 70)
    
    def calculate_entropy(data):
        counts = Counter(data)
        probs = [c/len(data) for c in counts.values()]
        return -sum(p * np.log2(p) for p in probs)

    from collections import Counter
    window = 100
    entropy_series = []
    for i in range(len(seq) - window):
        ent = calculate_entropy(seq[i:i+window])
        entropy_series.append(ent)
        
    print(f"    Overall Dataset Entropy: {calculate_entropy(seq):.4f}")
    print(f"    Peak Predictability (Min Entropy): {min(entropy_series):.4f}")
    print(f"    Peak Chaos (Max Entropy): {max(entropy_series):.4f}")
    
    # Detect Decades
    # We'll just show the last 5 windows to see current trend
    print(f"\n    Current Entropy Trend (Last 500 samples average): {np.mean(entropy_series[-5:]):.4f}")
    print("=" * 70)

if __name__ == "__main__":
    analyze_lags_and_entropy()
