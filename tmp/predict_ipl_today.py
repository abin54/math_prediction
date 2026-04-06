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
    
    # Match 1: DC vs MI (DC won toss, elected to BOWL)
    # So MI is BATTING first.
    print("\n[MATCH 1] DELHI CAPITALS vs MUMBAI INDIANS")
    print("Venue: Arun Jaitley Stadium, Delhi")
    print("Toss: DC won & elected to BOWL first.")
    master.run_forensic_ipl_audit(batting_team="MI", bowling_team="DC")
    
    # Match 2: GT vs RR
    # Toss not yet happened.
    print("\n[MATCH 2] GUJARAT TITANS vs RAJASTHAN ROYALS")
    print("Venue: Narendra Modi Stadium, Ahmedabad")
    master.run_forensic_ipl_audit(batting_team="GT", bowling_team="RR")

if __name__ == "__main__":
    predict_today()
