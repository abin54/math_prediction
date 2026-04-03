import pandas as pd
import numpy as np
from scipy import stats
import os

def get_total(v):
    try:
        v = int(pd.to_numeric(v, errors='coerce'))
        return (v // 10 + v % 10) % 10
    except:
        return -1

def decompose_series():
    file = "Number_Chart.xlsx"
    if not os.path.exists(file):
        print("File not found.")
        return
        
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    
    # 1. Day-of-the-Week Effect
    print("\n" + "="*70)
    print("  1. DAY-OF-THE-WEEK EFFECT ANALYSIS")
    print("-" * 70)
    
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    day_groups = {}
    for d in days:
        vals = pd.to_numeric(df[f"{d} Jodi Num"], errors='coerce').dropna().tolist()
        day_groups[d] = vals
        
    # Statistical test: Kruskal-Wallis (non-parametric ANOVA)
    h_stat, p_val = stats.kruskal(*[day_groups[d] for d in days])
    
    for d in days:
        avg = np.mean(day_groups[d])
        std = np.std(day_groups[d])
        print(f"    {d:3}: Mean={avg:5.2f} | Std={std:5.2f} | N={len(day_groups[d])}")
        
    print(f"\n    Kruskal-Wallis p-value: {p_val:.4f}")
    if p_val < 0.05:
        print("    RESULT: SIGNIFICANT (The Day of the Week MATTERS).")
    else:
        print("    RESULT: NOT SIGNIFICANT (Every day behaves the same).")

    # 2. Monthly / Seasonal Trends
    print("\n" + "="*70)
    print("  2. MONTHLY / SEASONAL TRENDS (52 YEARS)")
    print("-" * 70)
    
    # Extract month from Date Range
    def get_month(s):
        import re
        try:
            m = re.search(r'(\d{2})/(\d{2})/', str(s))
            return int(m.group(2))
        except:
            return 0
            
    df['Month'] = df['Date Range'].apply(get_month)
    # Combine all days into one to get monthly average
    df['WeeklyAvg'] = df[[f"{d} Jodi Num" for d in days]].mean(axis=1)
    monthly_stats = df.groupby('Month')['WeeklyAvg'].agg(['mean', 'std', 'count'])
    
    for m in range(1, 13):
        if m in monthly_stats.index:
            row = monthly_stats.loc[m]
            print(f"    Month {m:02}: Avg={row['mean']:5.2f} | Count={row['count']:3.0f}")

    # 3. Cyclical Patterns (FFT for hidden periods)
    print("\n" + "="*70)
    print("  3. CYCLICAL PATTERN DETECTION (X-Day Cycles)")
    print("-" * 70)
    
    # Flatten sequence
    sequence = []
    for idx, row in df.iterrows():
        for d in days:
            v = row[f"{d} Jodi Num"]
            if not pd.isna(v): sequence.append(float(v))
    
    seq = np.array(sequence)
    # Remove mean for FFT
    seq_detrended = seq - np.mean(seq)
    fft_vals = np.abs(np.fft.fft(seq_detrended))
    freqs = np.fft.fftfreq(len(seq))
    
    # Find dominant frequency (excluding first few noisy low frequencies)
    indices = np.where(freqs > 0)[0]
    dominant_idx = indices[np.argmax(fft_vals[indices])]
    dominant_period = 1 / freqs[dominant_idx]
    
    print(f"    Primary Cycle detected: Every {dominant_period:.2f} days.")
    print(f"    This suggests the chart 'Resets' its pattern every ~{int(round(dominant_period))} days.")
    print("=" * 70)

if __name__ == "__main__":
    decompose_series()
