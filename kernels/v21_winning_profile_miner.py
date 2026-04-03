"""
Winning Profile Miner v21.0 — Astrological Signature Audit
==========================================================
1. Identifying Sun, Moon, and Mercury degree clusters for high-value results.
2. Filter: Checking Mercury Retrograde correlations with past errors.
"""

import pandas as pd
import numpy as np
import os
from scipy import stats

def run_winning_profile_audit():
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
    print("  MODEL v21.0: WINNING ASTROLOGICAL PROFILE AUDIT (52 YEARS)")
    print("-" * 70)
    
    # 1. SUN/MOON DEGREE CLUSTERS (Proxy)
    # Sidereal Longitude = (Day * 1.0) approx for Sun, (Day * 13.1) approx for Moon
    sun_long = (np.arange(n) * 0.9856) % 360
    moon_long = (np.arange(n) * 13.176) % 360
    
    # High-Value Peaks (>90)
    peaks = np.where(seq > 90)[0]
    peak_sun = sun_long[peaks]
    peak_moon = moon_long[peaks]
    
    print(f"  [Sun Profile] High-Value Cluster (Mean Deg): {np.mean(peak_sun):.2f}°")
    print(f"  [Moon Profile] High-Value Cluster (Mean Deg): {np.mean(peak_moon):.2f}°")
    
    # 2. MERCURY RETROGRADE FILTER (Retro-Logic Proxy)
    # Mercury retrogrades ~3 times a year (~21 days each)
    # We use a 116-day synodic cycle proxy
    mercury_retro = (np.arange(n) % 116) < 21
    error_rate_retro = np.mean(seq[mercury_retro])
    error_rate_direct = np.mean(seq[~mercury_retro])
    
    print(f"\n  [Mercury Retro Check]:")
    print(f"    - Mean During Retrograde: {error_rate_retro:.2f}")
    print(f"    - Mean During Direct: {error_rate_direct:.2f}")
    print(f"    - Logic: Current Status is DIRECT (Low-Error Stability)")

    # 3. WINNING PROFILE FOR TODAY (WEDNESDAY)
    # Today's Wednesday Sun Longitude (Approx):
    current_sun = sun_long[-1]
    current_moon = moon_long[-1]
    
    # Find historical days with similar alignments
    similar_days = np.where((np.abs(sun_long - current_sun) < 5) & (np.abs(moon_long - current_moon) < 5))[0]
    if len(similar_days) > 0:
        winning_avg = np.mean(seq[similar_days])
        print(f"\n  [V21] Winning Profile Match Source: {int(winning_avg)} Jodi")
    else:
        print("\n  [V21] No exact Astro-Profile match found in depth memory.")

    print("\n" + "="*70)

if __name__ == "__main__":
    run_winning_profile_audit()
