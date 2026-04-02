"""
Matrix Statistical Synthesizer v1.0
===================================
Automates the 'Mode-Mean-Consensus' analysis.
Analyzes the 'Observation Matrix' to find the statistical consensus.
Outputs the final 'Statistical Mode' result.
"""

import os, json
from collections import Counter

def run_matrix_synthesis(matrix_file):
    print("\n" + "="*80)
    print("  MATRIX STATISTICAL SYNTHESIS — THE CONSENSUS LAYER")
    print("="*80)

    # 1. LOAD MATRIX
    try:
        with open(matrix_file, "r") as f:
            matrix = json.load(f)
    except Exception as e:
        print(f"Error loading {matrix_file}: {e}")
        return

    results = [int(item['result']) for item in matrix if item['status'] == "SUCCESS"]
    
    # 2. STATISTICAL SYNTHESIS (Mode & Mean)
    if not results:
        print("    [ERROR] No successful results present in matrix.")
        return None

    # Finding Mode
    data = Counter(results)
    mode_v = data.most_common(1)[0][0]
    frequency = data.most_common(1)[0][1]
    
    # Finding Mean
    mean_v = sum(results) / len(results)
    
    print(f"\n  [PHASE 3] SYNTHESIS (Analysis Results):")
    print(f"    - Statistical Mode (Most Frequent): {mode_v:02d} (Frequency: {frequency}/{len(results)})")
    print(f"    - Statistical Mean (Average): {mean_v:.2f}")

    # 3. FINAL CONCLUSION (Statistical Mode)
    consensus_v = mode_v
    print(f"\n  [PHASE 4] FINAL CONCLUSION (Statistical Consensus):")
    print(f"    >>> Status: Consolidated Consensus achieved.")
    print(f"    >>> Winner for today (16-Reflector Law): {consensus_v:02d}")
    print("="*80 + "\n")
    
    return consensus_v

if __name__ == "__main__":
    run_matrix_synthesis("observation_matrix.json")
