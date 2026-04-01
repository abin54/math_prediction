import pandas as pd
import numpy as np
import os
from scipy.fft import fft, fftfreq

def run_celestial_resonance_audit():
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
    print("  MODEL v19.0: CELESTIAL RESONANCE AUDIT (52 YEARS)")
    print("-" * 70)
    
    # 1. FOURIER SYNODIC FREQUENCIES
    yf = fft(seq - np.mean(seq))
    xf = fftfreq(n, 1) # 1 day per step
    # We look for periods (1/freq)
    # Jupiter (11.8 yrs = 4307 days), Saturn (29.4 yrs = 10731 days)
    # 20-year cycle (7300 days), 9.0-day cycle (found previously)
    
    amplitudes = np.abs(yf)
    top_indices = np.argsort(amplitudes)[::-1][1:10] # Top 10 frequencies (skip DC)
    
    print(f"  [Synodic Resonance] Top Frequencies Identified:")
    for i in top_indices:
        freq = np.abs(xf[i])
        if freq > 0:
            period = 1/freq
            days_val = period
            years_val = period/365.25
            print(f"    - Period: {days_val:7.1f} days ({years_val:4.2f} years) | Amp: {amplitudes[i]:.2f}")
            
    # 2. CELESTIAL MAPPING (Jupiter/Saturn 50-Year Cycle)
    # The 52-year sequence covers almost two full Jupiter cycles (12x2=24)
    # and nearly two Saturn cycles (29.4x2=58.8). 
    # High resonance around 10-12 years is a "Jupiter Anchor."
    
    jupiter_idx = np.argmin(np.abs(1/xf[1:] - 4307))
    saturn_idx = np.argmin(np.abs(1/xf[1:] - 10731))
    
    print(f"\n  [Planetary Sync Error]:")
    print(f"    - Jupiter Sync (4307d): {amplitudes[jupiter_idx]:.2f} magnitude")
    print(f"    - Saturn Sync (10731d): {amplitudes[saturn_idx]:.2f} magnitude")

    print("\n" + "="*70)

if __name__ == "__main__":
    run_celestial_resonance_audit()
