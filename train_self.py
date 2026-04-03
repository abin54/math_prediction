"""
Training Brain v1.0 — Autonomous Weight Optimizer
===============================================
1. Runs a Walk-Forward Validation (WFV) across the last 60 days.
2. Evaluates every agent's "Hit Rate" in the Top 4.
3. Automatically generates optimized_weights.json.
"""

import os, json, datetime
import pandas as pd
import numpy as np
from swarm_predictor import StatAgent, TrendAgent, TransitionAgent, CycleAgent, MirrorTraceAgent, SeriesSpikeAgent, StepAgent, MLAgent

AGENTS = [
    StatAgent(), TrendAgent(), TransitionAgent(), CycleAgent(), 
    MirrorTraceAgent(), SeriesSpikeAgent(), StepAgent()
]

def run_self_training(days_back=10):
    print("\n" + "="*70)
    print(f"  TRAINING BRAIN: OPTIMIZING AGENT WEIGHTS (Last {days_back} insertions)")
    print("="*70)
    
    # Load dataset
    df = pd.read_excel("Number_Chart.xlsx", sheet_name="Sheet1")
    results = {}
    for day in ["MON", "TUE", "WED", "THU", "FRI", "SAT"]:
        col = f"{day} Jodi Num"
        if col in df.columns:
            results[day] = df[col].dropna().astype(int).tolist()
            
    # Track scores for each agent
    agent_scores = {a.name: 0 for a in AGENTS}
    agent_tests = {a.name: 0 for a in AGENTS}
    
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    
    # Iterate backwards through time
    # We'll test the last 60 entries of 'Monday' to represent 60 weeks
    for i in range(-days_back, 0):
        try:
            for day_idx, day in enumerate(days):
                target_val = results[day][i]
                
                # Get the previous day result
                if day == "MON":
                    # Previous was Saturday of the previous entry
                    prev_val = results["SAT"][i-1]
                    prev_day = "SAT"
                else:
                    prev_val = results[days[day_idx-1]][i]
                    prev_day = days[day_idx-1]
                
                # Test every agent
                current_day_history = results[day][:i] # Hide the future
                yesterday_history = results[prev_day][:i]
                
                for agent in AGENTS:
                    try:
                        preds = agent.predict(
                            target_day_vals=current_day_history,
                            yesterday_vals=yesterday_history,
                            yesterday_jodi=prev_val,
                            target_day=day,
                            yesterday_day=prev_day
                        )
                        top4 = [p[0] for p in preds[:4]]
                        if target_val in top4:
                            agent_scores[agent.name] += 1
                        agent_tests[agent.name] += 1
                    except: pass
        except: continue

    # Calculate Weights based on Hit Rate
    weights = {}
    total_hits = sum(agent_scores.values())
    
    if total_hits == 0:
        print("  [WARNING] No hits detected in training period. Using defaults.")
        return
        
    print("\n  [TRAINING RESULTS - HIT RATES]:")
    for name, hits in agent_scores.items():
        rate = hits / agent_tests[name] if agent_tests[name] > 0 else 0
        print(f"    - {name:18}: {hits}/{agent_tests[name]} ({rate:.1%})")
        # Base weight on relative performance
        weights[name] = round(hits / total_hits, 3)

    # Ensure weights sum to 0.85 (leave 0.10 for MLAgent and 0.05 for LLMAgent)
    sum_w = sum(weights.values())
    for name in weights:
        weights[name] = round((weights[name] / sum_w) * 0.85, 3)
        
    # Add fixed baselines
    weights["MLAgent"] = 0.10
    weights["LLMAgent"] = 0.05
    
    # Save to file
    with open("optimized_weights.json", "w") as f:
        json.dump(weights, f, indent=4)
        
    print(f"\n  [SUCCESS] optimized_weights.json generated.")
    print("="*70 + "\n")

if __name__ == "__main__":
    run_self_training()
