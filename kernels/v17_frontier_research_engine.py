"""
Frontier Research Engine v17.0 — The 2026 Synthesis Engine
==========================================================
1. Wavelet Decomposition: Macro trends vs. Daily noise.
2. ODE Derivative: Continuous Logic Flow.
3. Score-Based Density: Generative Map for the next Jodi.
4. SAM Stability check: Sharpness-Aware neighborhood volatility.
"""

import pandas as pd
import numpy as np
import os
from scipy import signal, stats

def run_frontier_synthesis():
    file = "Number_Chart.xlsx"
    if not os.path.exists(file):
        print("File not found.")
        return
        
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    sequence = []
    days_cols = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    
    # Flatten history (Business days only)
    for idx, row in df.iterrows():
        for d in days_cols:
            v = str(row[f"{d} Jodi Num"]).strip()
            if "★" not in v and v != "" and v != "nan" and v != " " and v != "None":
                sequence.append(float(v))
            
    seq = np.array(sequence)
    n = len(seq)
    
    print("\n" + "="*70)
    print("  MODEL v17.0: THE FRONTIER RESEARCH ENGINE (PROXIES)")
    print("-" * 70)
    
    # 1. WAVELET DECOMPOSITION (Proxy)
    # Using scipy.signal.windows.gaussian (Fixed the AttributeError)
    from scipy.signal import windows
    window = windows.gaussian(51, std=7)
    trend = signal.convolve(seq, window / window.sum(), mode='same')
    detrended = seq - trend
    
    print(f"  [Wavelet] 52-Year Decomposition:")
    print(f"    - Macro Trend (Approximation): Mean {np.mean(trend):.2f}")
    print(f"    - Daily Noise (Detail): Mean {np.mean(detrended):.2f}")
    
    # 2. NEURAL ODE FLOW (Proxy)
    # Derivative of the hidden state (dh/dt)
    dhdt = np.gradient(trend)
    print(f"  [Neural ODE] Continuous Momentum (dh/dt): {dhdt[-1]:.4f}")
    
    # 3. SCORE-BASED DENSITY (Diffusion Proxy)
    # Finding the probability density of the current state
    density = stats.gaussian_kde(seq)
    x_range = np.arange(0, 100)
    target_score = x_range[np.argsort(density(x_range))[-1]]
    
    print(f"  [Diffusion] Target Denoised Score: {target_score}")
    
    # 4. SAM STABILITY CHECK
    # Calculate neighborhood volatility
    current_vol = np.std(seq[-10:])
    print(f"  [SAM] Neighborhood Stability: {current_vol:.2f}")

    # FINAL FRONTIER SYNTHESIS (WEDNESDAY)
    # Yesterday TUE = 04. Today is WED.
    # Prediction = (Trend + (Deriv * Step) + Denoised_Score) / 2
    final_pred = (trend[-1] + (dhdt[-1] * 1) + target_score) / 2.0
    
    print("\n" + "="*70)
    print("  THE FRONTIER VERDICT: TIER-1 SYNTHESIS")
    print("-" * 70)
    print(f"  Frontier State Prediction (Wednesday): {final_pred:.2f}")
    
    # Candidate Jodis for Wednesday
    candidates = [int(final_pred), int(final_pred)+1, int(final_pred)-1]
    print(f"\n  [FRONT] High-Capacity Jodis: {candidates}")
    print("=" * 70)

if __name__ == "__main__":
    run_frontier_synthesis()
