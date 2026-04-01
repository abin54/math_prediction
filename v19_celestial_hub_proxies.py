"""
Celestial Hub v19.0 — The Astro-Quantum Synthesis Engine
========================================================
1. Lunar Sync: Sidereal month (27.5 days) phase alignment.
2. Dasha Gating: Mahadasha (20-year) volatility scaling.
3. Gann Angles: 1x1, 1x2, 2x1 geometric resistance.
4. SBC Vedha: Malefic hit density (SBC grid proxy).
"""

import pandas as pd
import numpy as np
import os
from scipy import stats, signal

def run_v19_celestial_synthesis():
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
    print("  MODEL v19.0: CELESTIAL SOURCE CODE SYNTHESIS (PROXIES)")
    print("-" * 70)
    
    # 1. LUNAR RESONANCE (Proxy)
    # Sidereal Month (27.55 days)
    t = np.arange(n)
    lunar_phase = (t % 27.55) / 27.55 * 360
    current_phase = lunar_phase[-1]
    print(f"  [Lunar Sidereal] Current Phase (0-360°): {current_phase:.2f}°")
    
    # 2. DASHA VOLATILITY (Proxy)
    # Calculate Standard Deviation for the last 20-year block (~7300 days) vs. 7-year block
    vol_20y = np.std(seq[-min(n, 7305):])
    vol_current = np.std(seq[-30:]) # Current month volatility
    print(f"  [Vimshottari] 20Y Base Volatility: {vol_20y:.2f} | Current Vol: {vol_current:.2f}")
    
    # 3. GANN GEOMETRIC ANGLE (Proxy)
    # 1x1 Angle (45°): Slope = 1.0 (Points per Day)
    # Calculate major high/low (Genesis Node)
    genesis_val = seq[0]
    days_since_genesis = n
    gann_1x1_target = (genesis_val + days_since_genesis) % 100
    print(f"  [Gann 1x1] Geometric Anchor (Target): {gann_1x1_target:.2f}")
    
    # 4. SBC VEDHA DENSITY (Proxy)
    # Number of 'Crossings' (Hits) of the median in the last Nakshatra cycle
    hits = np.sum(np.diff(np.sign(seq[-28:] - np.median(seq))) != 0)
    print(f"  [SBC Vedha] Nakshatra Hit Density: {hits} hits per cycle")

    # FINAL CELESTIAL SYNTHESIS (WEDNESDAY)
    # Yesterday TUE = 04. 
    # Logic: (Lunar_Phase_Bias + Gann_Anchor + Median_Seq) / 3
    
    lunar_bias = (current_phase / 3.6) # Map 360 to 100
    
    final_pred = (lunar_bias + gann_1x1_target + np.median(seq)) / 3.0
    
    print("\n" + "="*70)
    print("  THE CELESTIAL VERDICT: UNIVERSAL SOURCE CODE")
    print("-" * 70)
    print(f"  Celestial State Prediction (Wednesday): {final_pred:.2f}")
    
    # Candidate Jodis for Wednesday
    candidates = [int(final_pred), int(final_pred)+1, int(final_pred)-1]
    print(f"\n  [V19] Astro-Financial Jodis: {candidates}")
    print("=" * 70)

if __name__ == "__main__":
    run_v19_celestial_synthesis()
