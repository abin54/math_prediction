import os
import sys

# Ensure root is in path
sys.path.append(os.getcwd())

from Sovereign_IPL_Master import SovereignIPLMaster

def predict_today():
    master = SovereignIPLMaster()
    
    print("\n" + "="*80)
    print("  IPL TODAY: SUPREME FORENSIC PREDICTIONS (APRIL 4, 2026)")
    print("="*80)
    
    # Match 1: DC vs MI (COMPLETED)
    print("\n[MATCH 1] DELHI CAPITALS vs MUMBAI INDIANS (RESULT: DC WON)")
    print("Venue: Arun Jaitley Stadium, Delhi")
    print("Outcome: DC chased 163 in 18.1 overs. Sameer Rizvi 90(51).")
    
    # Match 2: GT vs RR (UPCOMING / LIVE)
    print("\n[MATCH 2] GUJARAT TITANS vs RAJASTHAN ROYALS")
    print("Venue: Narendra Modi Stadium, Ahmedabad")
    print("Toss: RR won & elected to BAT first.")
    print("Forensic Note: Shubman Gill (GT) is OUT due to muscle spasm. Rashid Khan is captaining.")
    
    # Setting RR as batting team and GT as bowling team
    master.run_forensic_ipl_audit(batting_team="RR", bowling_team="GT")

if __name__ == "__main__":
    predict_today()
