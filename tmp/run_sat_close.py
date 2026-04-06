import sys
import os

# Add the project root to sys.path
sys.path.append(r'f:\PROJECTS\MATH PREDICTION')

from Sovereign_Judge_Master import SovereignJudgeMaster

def run_final_sat_prediction():
    master = SovereignJudgeMaster()
    # Explicitly setting Open to 2 as per user finding
    jodi = master.proclaim_sovereignty(fixed_open=2)
    print(f"\nFINAL VERDICT: {jodi}")

if __name__ == "__main__":
    run_final_sat_prediction()
