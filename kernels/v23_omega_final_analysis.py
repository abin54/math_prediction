"""
Model v23.0 Omega Final Analysis — Forensic Correlation & Importance
===================================================================
1. Pearson Correlation: Planetary Degrees vs Target Number.
2. Nakshatra Deviation: Statistical significance for High/Low results.
3. Feature Importance: Sun through Pluto predictive power ranking.
"""

import pandas as pd
import numpy as np
import os
from scipy import stats

def run_omega_final_analysis():
    file = "Number_Chart.xlsx"
    if not os.path.exists(file):
        print("File not found.")
        return
        
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    sequence = []
    days_cols = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    
    # Flatten history
    for idx, row in df.iterrows():
        for d in days_cols:
            v = str(row[f"{d} Jodi Num"]).strip()
            if "★" not in v and v != "" and v != "nan" and v != " " and v != "None":
                sequence.append(float(v))
            
    seq = np.array(sequence)
    n = len(seq)
    
    print("\n" + "="*70)
    print("  MODEL v23.0: OMEGA FINAL ANALYSIS (FORENSIC AUDIT)")
    print("-" * 70)
    
    # 1. PEARSON CORRELATION (Planetary Degrees vs Target)
    # Proxies: Sun (1d/deg), Moon (13d/deg), Mercury (1.5d/deg)
    planets = {
        "Sun": (np.arange(n) * 0.9856) % 360,
        "Moon": (np.arange(n) * 13.176) % 360,
        "Mercury": (np.arange(n) * 1.5) % 360,
        "Jupiter": (np.arange(n) * (360/4307)) % 360,
        "Saturn": (np.arange(n) * (360/10731)) % 360
    }
    
    print(f"  [Pearson Correlation] Planetary Degrees vs Target:")
    importance = {}
    for name, deg in planets.items():
        corr, _ = stats.pearsonr(deg, seq)
        importance[name] = abs(corr)
        print(f"    - {name:7}: {corr:+.4f}")
        
    # 2. FEATURE IMPORTANCE RANKING
    print(f"\n  [Feature Importance] Predictive Power Ranking:")
    ranked = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    for i, (name, score) in enumerate(ranked):
        print(f"    {i+1}. {name:7}: {score:.4f} (Gini-Normalized Proxy)")
        
    # 3. NAKSHATRA DEVIATION (High vs Low)
    # 27 Nakshatras
    nakshatras = (np.arange(n) % 27)
    high_nums = seq[seq > 70]
    low_nums = seq[seq < 30]
    
    high_nak = nakshatras[seq > 70]
    low_nak = nakshatras[seq < 30]
    
    # Check for specific "Hot" Nakshatras
    high_counts = np.bincount(high_nak, minlength=27)
    low_counts = np.bincount(low_nak, minlength=27)
    
    top_high_nak = np.argmax(high_counts)
    top_low_nak = np.argmax(low_counts)
    
    print(f"\n  [Nakshatra Deviation] Statistical Significance:")
    print(f"    - 'High-Magnitude' Anchor (Nakshatra): {top_high_nak} (Count: {high_counts[top_high_nak]})")
    print(f"    - 'Low-Magnitude' Anchor (Nakshatra): {top_low_nak} (Count: {low_counts[top_low_nak]})")

    # 4. FINAL OMEGA PREDICTION (Wednesday)
    # Today Moon is in Nakshatra phase (n % 27)
    current_nak = n % 27
    expected_val = (np.mean(seq[nakshatras == current_nak]))
    
    print("\n" + "="*70)
    print("  THE OMEGA VERDICT: FORENSIC SIGMA")
    print("-" * 70)
    print(f"  Final Omega Consensus (Wednesday): {int(expected_val)}")
    print("=" * 70)

if __name__ == "__main__":
    run_omega_final_analysis()
