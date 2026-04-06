import os
import sys
import numpy as np

# Ensure root is in path
sys.path.append(os.getcwd())

from Sovereign_IPL_Master import SovereignIPLMaster

def project_mi_final():
    master = SovereignIPLMaster()
    
    print("\n" + "="*80)
    print("  IPL FORENSIC PROJECTION: MI FINAL 20-OVER SCORE")
    print("="*80)
    
    # Starting Point: 68/2 after 8.4 overs (approx 8.6 balls)
    current_runs = 68
    current_wickets = 2
    current_overs = 8.66 # 8.4 overs = 52 balls. 52/6 = 8.66
    
    # Historical RPO pulse: 
    # Over 1-6: 41 runs (6.83 RPO)
    # Over 7-9: 27 runs in 2.66 overs (10.15 RPO - Acceleration)
    historical_pulse = [8.0, 10.0, 0.0, 7.0, 7.0, 9.0, 11.0, 10.0, 9.0]
    
    # Generate projection for the next 11 overs (to reach 20.0 overs)
    horizon = 11
    projections = master.foundation.forecast(historical_pulse, horizon=horizon)
    
    print(f"\n[CURRENT STATE] MI: {current_runs}/{current_wickets} in {current_overs:.1f} overs (RR: {current_runs/current_overs:.2f})")
    print(f"[MODEL] TimesFM-2.5 Foundation Engine projection active...")
    
    total_projected = current_runs
    for i, rr in enumerate(projections, 1):
        total_projected += rr
    
    print("\n" + "-"*40)
    print(f"  PROJECTED 20-OVER SCORE: {int(total_projected)} - {int(total_projected + 15)}")
    print(f"  EXPECTED BACK-END RPO (OVERS 10-20): {np.mean(projections):.2f}")
    print("-" * 40)
    
    # Win Probability Phase
    # DC vs MI at Delhi.
    # Pitch: High scoring ground.
    # Target in 160-170 range is usually 45-50% win prob.
    
    win_prob = 0.52 # Baseline for MI if score > 165
    if total_projected > 175:
        win_prob = 0.64
    elif total_projected < 155:
        win_prob = 0.38
        
    print(f"\n  SUPREME VERDICT: MI WIN PROBABILITY: {win_prob*100:.1f}%")
    print(f"  RECOMMENDED ACTION: {'HOLD' if 0.45 < win_prob < 0.55 else 'BACK MI' if win_prob >= 0.55 else 'LAY MI'}")
    print("="*80 + "\n")

if __name__ == "__main__":
    project_mi_final()
