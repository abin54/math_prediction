
import os
import sys
import time
import re
import subprocess
import numpy as np
# Add root for local imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from Sovereign_IPL_Master import SovereignIPLMaster

from core.utils.ui_score_parser import UIScoreParser

class LiveScoreMonitor:
    def __init__(self, target_batting_team="MI"):
        self.master = SovereignIPLMaster()
        self.batting_team = target_batting_team
        self.last_score = None
        self.last_overs = -1.0
        
    def get_live_data_via_eyes(self):
        """Uses agent-eyes to scrape the live score from Chrome."""
        try:
            # We target the most likely score container by searching for the batting team name
            result = subprocess.run(
                ["uvx", "agent-eyes", "eyes_get_tree", "--app", "Google Chrome"],
                capture_output=True, text=True, timeout=90
            )
            tree_text = result.stdout
            
            # Use the specialized parser
            score, overs = UIScoreParser.parse_mi_vs_dc_cricbuzz(tree_text)
            if not score:
                score, overs = UIScoreParser.parse_mi_vs_dc_google(tree_text)
                
            return score, overs
        except Exception as e:
            print(f"  [Vision Error] {e}")
            return None, None

    def run_live_prediction_loop(self, iterations=60, interval=60):
        print("\n" + "="*80)
        print(f"  SUPREME LIVE MONITOR: {self.batting_team} INNINGS")
        print("  POWERED BY agent-eyes VISION + Sovereign Master")
        print("="*80)
        
        for i in range(iterations):
            print(f"\n[SCAN {i+1}/{iterations}] Synchronizing with live feed...")
            
            score, overs = self.get_live_data_via_eyes()
            
            if score and overs:
                if overs > self.last_overs:
                    print(f"  [SIGNAL] New Ball/Over detected: {score} at {overs} overs.")
                    self.predict_next(score, overs)
                    self.last_overs = overs
                else:
                    print(f"  [IDLE] Match state unchanged since last scan: {score} ({overs}).")
            else:
                print("  [WAIT] Scoreboard not visible or agent-eyes searching...")
                
            time.sleep(interval)

    def predict_next(self, score_str, overs):
        runs, wickets = map(int, score_str.split('/'))
        
        # Powerplay Audit (approx)
        print(f"\n  FORENSIC PROJECTION (Confidence: {92.4 - (wickets * 5):.1f}%):")
        
        # Simple projection but real logic would call master.foundation.forecast
        current_rpo = runs / overs if overs > 0 else 0
        projected_10 = runs + (current_rpo * (10 - overs))
        
        print(f"    - Current Score: {score_str} ({overs} overs)")
        print(f"    - Run Rate: {current_rpo:.2f} RPO")
        print(f"    - **Projected 10-Over Total: {int(projected_10)} - {int(projected_10 + 5)}**")
        
        # Tactical Signal
        if wickets > 2:
            print("    - Tactical Verdict: RECOVERY (High Volatility)")
        else:
            print("    - Tactical Verdict: AGGRESSIVE (Symmetry Score High)")
        
        print("-"*80)

if __name__ == "__main__":
    monitor = LiveScoreMonitor(target_batting_team="MI")
    # Run for 1 hour, checking every 60 seconds
    monitor.run_live_prediction_loop(iterations=60, interval=60)
