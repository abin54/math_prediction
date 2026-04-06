import os
import sys
import numpy as np

# Ensure root is in path
sys.path.append(os.getcwd())

from Sovereign_IPL_Master import SovereignIPLMaster

def project_mi_score():
    master = SovereignIPLMaster()
    
    print("\n" + "="*80)
    print("  IPL FORENSIC PROJECTION: MI 10-OVER SCORE")
    print("="*80)
    
    # Starting Point: 18/1 after 3 overs (Live Update 3:45 PM IST)
    # WICKET: Ryan Rickelton fell in the 3rd over.
    current_runs = 18
    current_wickets = 1
    current_overs = 3.0
    
    # Run rates so far: 8.0, 10.0, 0.0 (Wicket/Maiden over)
    historical_pulse = [8.0, 10.0, 0.0]
    
    # Generate projection for the next 7 overs (to reach 10.0 overs)
    horizon = 7
    projections = master.foundation.forecast(historical_pulse, horizon=horizon)
    
    print(f"\n[CURRENT STATE] MI: {current_runs}/{current_wickets} in {current_overs} overs (RR: {current_runs/current_overs:.2f})")
    print(f"[MODEL] TimesFM-2.5 Foundation Engine projection active...")
    
    total_projected = current_runs
    for i, rr in enumerate(projections, 1):
        total_projected += rr
    
    print("\n" + "-"*40)
    print(f"  PROJECTED 10-OVER SCORE: {int(total_projected)} - {int(total_projected + 12)}")
    print(f"  EXPECTED RUN RATE (OVERS 2-10): {np.mean(projections):.2f}")
    print("-"*40)
    
    # Symmetry Audit
    print("\n[AUDIT] Assessing Arun Jaitley Stadium 'Powerplay Momentum'...")
    if np.mean(projections) > 9.5:
        print("    - Verdict: HYPER-AGGRESSIVE (Likely Rohit Sharma effect)")
    elif np.mean(projections) > 8.5:
        print("    - Verdict: STEADY POWERPLAY (Standard Delhi Curve)")
    else:
        print("    - Verdict: CONSERVATIVE (Delhi pitch showing early grip)")
    print("="*80 + "\n")

if __name__ == "__main__":
    project_mi_score()
