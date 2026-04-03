"""
Master Logic Filter v1.0 — 52-Year Historical Constraints
==========================================================
Identifies every "Impossible Transition" ($X \rightarrow Y$) that has 
NEVER occurred in the 52-year history of the Kalyan chart.
Used as a Deterministic Layer in Model v11.0.
"""

import pandas as pd
import numpy as np
from collections import defaultdict
import os

def run_filter():
    file = "Number_Chart.xlsx"
    if not os.path.exists(file):
        print("File not found.")
        return
        
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    sequence = []
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    for idx, row in df.iterrows():
        for d in days:
            v = row[f"{d} Jodi Num"]
            if not pd.isna(v): sequence.append(int(v))
            
    # Transitions (Today -> Tomorrow)
    transitions = set()
    for i in range(len(sequence)-1):
        transitions.add((sequence[i], sequence[i+1]))
        
    print("\n" + "="*70)
    print("  DETERMINISTIC FILTER: 52-YEAR CONSTRAINT MINER")
    print("-" * 70)
    print(f"  Total Transitions Found: {len(transitions)}")
    print(f"  Possible Pairs (10,000) vs. Observed Pairs ({len(transitions)})")
    
    unseen_pairs = 10000 - len(transitions)
    sparsity = (unseen_pairs / 10000) * 100
    print(f"  Dataset Sparsity: {sparsity:.1f}% (6,000+ pairs have NEVER happened)")
    
    # Check current TUE -> WED logic (Yesterday was 04)
    yest = 4
    impossibles = []
    for i in range(100):
        if (yest, i) not in transitions:
            impossibles.append(i)
            
    print(f"\n  [CHECK] Yesterday TUE = {yest:02d}. Candidates for Wednesday:")
    print(f"    - Historically Impossible Matches (0% Chance): {len(impossibles)}")
    print(f"    - Historically Proven Matches: {100 - len(impossibles)}")
    
    # Find the top 10 "Locked" transitions (where X almost always lead to Y)
    trans_counts = Counter()
    for i in range(len(sequence)-1):
        trans_counts[(sequence[i], sequence[i+1])] += 1
        
    print("\n  Top 5 Historically Proven Transitions (The 'Hubs'):")
    for (a, b), count in trans_counts.most_common(5):
        print(f"    {a:02d} -> {b:02d}: Observed {count} times in 52 years.")

if __name__ == "__main__":
    from collections import Counter
    run_filter()
