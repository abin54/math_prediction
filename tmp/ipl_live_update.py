import os
import sys

# Ensure root is in path
sys.path.append(os.getcwd())

from Sovereign_IPL_Master import SovereignIPLMaster

def update_prediction():
    master = SovereignIPLMaster()
    
    print("\n" + "="*80)
    print("  IPL LIVE UPDATE: FORENSIC RE-CALIBRATION (APRIL 4, 2026)")
    print("="*80)
    
    # Current Match 2: RR vs GT
    # RR: 69/0 (6.0 overs)
    print("\n[LIVE] RAJASTHAN ROYALS vs GUJARAT TITANS")
    print("Score: RR 69/0 (6.0 Overs)")
    
    # Using stream_predict for live analytics
    next_rr, wicket_prob = master.stream_predict(current_score="69/0", current_overs=6.0)
    
    print("\n" + "="*80)
    print(f"  SUPREME FORENSIC UPDATE (RR vs GT)")
    print(f"  Projected Run Rate (Next Over): {next_rr:.2f}")
    print(f"  Wicket Probability (Next Phase): {wicket_prob*100:.1f}%")
    print(f"  Current Momentum: EXTREME BULLISH (RR)")
    print("="*80)

if __name__ == "__main__":
    update_prediction()
