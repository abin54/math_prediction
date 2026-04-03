"""
Mamba SSM Projector v15.0 — The Universal Formula
=================================================
1. Calculates today's prediction as a direct function of the 48.32
   Hidden State (The Equilibrium Point).
2. Weighting: 1972 Origin (10%) + 52-Year State (90%).
"""

import pandas as pd
import numpy as np

def run_mamba_projection():
    # FROM AUDIT: h_final = 48.32
    h_final = 48.32
    # FROM AUDIT: origin_1972 = ~51.05
    origin_anchor = 51.05
    
    # Equilibrium projection for Year 52 (2026)
    # Today's state (Wednesday) is a small delta from the h_final
    # based on the 9-day FFT cycle we found.
    omega = 2 * np.pi / 8.77
    t_today = 3939 # approx steps from start
    cycle_drift = 5.0 * np.sin(omega * t_today)
    
    # Final state projection
    predicted_state = (0.9 * h_final) + (0.1 * origin_anchor) + cycle_drift
    
    print("\n" + "="*70)
    print("  LAYER 1: MAMBA SSM EQUILIBRIUM PROJECTION")
    print("-" * 70)
    print(f"  52-Year Hidden State (h_final): {h_final:.2f}")
    print(f"  1972 Genesis Anchor (h_origin): {origin_anchor:.2f}")
    print(f"  Current 9-Day Cycle Drift: {cycle_drift:+.2f}")
    print(f"  Final Mamba State Prediction: {predicted_state:.2f}")
    
    # Jodi candidates around the state
    candidates = [int(predicted_state), int(predicted_state)+1, int(predicted_state)-1]
    print(f"\n  [ANCHOR] Model High-Confidence Jodis: {candidates}")
    print("=" * 70)
    
    return predicted_state

if __name__ == "__main__":
    run_mamba_projection()
