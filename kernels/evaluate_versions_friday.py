import pandas as pd
import numpy as np
from collections import Counter
import os

# --- CONTEXT ---
YESTERDAY_JODI = 16
OPEN_VAL = 1
CLOSE_VAL = 6
TARGET_DAY = "FRI"
SEQUENCE_UPDATE = [74, 4, 19, 16] # Mon, Tue, Wed, Thu

def load_full_sequence():
    file = "Number_Chart.xlsx"
    if not os.path.exists(file):
        return []
    try:
        df = pd.read_excel(file, sheet_name="Sheet1")
        sequence = []
        days_cols = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
        for _, row in df.iterrows():
            for d in days_cols:
                col_name = f"{d} Jodi Num"
                if col_name in df.columns:
                    v = str(row[col_name]).strip()
                    if v and v != "nan" and "★" not in v:
                        try:
                            sequence.append(float(v))
                        except: pass
        # Append this week's known results
        return sequence + SEQUENCE_UPDATE
    except Exception as e:
        print(f"Error loading sequence: {e}")
        return SEQUENCE_UPDATE

def get_v16_logic(yesterday=16):
    # v16 Geneis Pulse (Baseline ~48.60)
    base_state = 48.60 
    # Historical followers of 16 on Friday
    candidates = [35, 85, 30, 80, 16, 61]
    favored = sorted(candidates, key=lambda x: abs(x - base_state))
    return {favored[0]: 0.50, favored[1]: 0.30, favored[2]: 0.20}

def get_v26_logic(yesterday=16):
    # Symmetry Focused (1->6, 6->1)
    # 16 Mirror is 61. Family is 11, 66, 61, 16.
    # Friday Resonance usually shifts +2 or +5
    # 1+2=3, 1+5=6. 6+2=8, 6+5=1.
    return {35: 0.40, 85: 0.35, 68: 0.25}

def get_v35_logic(seq):
    # Hypergraph GNN / Sequence based
    # Top Frequency in recent 100
    recent = seq[-100:]
    c = Counter(recent)
    top = c.most_common(3)
    res = {}
    total = sum(cnt for val, cnt in top)
    for val, cnt in top:
        res[int(val)] = cnt / total
    return res

def get_v40_logic(seq):
    # Topos / Motive / Abraxas
    n = len(seq)
    heyting = (np.mean(seq[-24:]) + (n % 100)) % 100
    motivic = (np.std(seq[-52:]) * 1.732) % 100
    abraxas = (np.mean(seq) * (365/52) / 7) % 100
    pred = (heyting * 0.3 + motivic * 0.3 + abraxas * 0.4) % 100
    p = int(pred)
    # Mirror set
    MIRROR = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}
    def get_full_cut(n):
        t, u = n // 10, n % 10
        return MIRROR[t] * 10 + MIRROR[u]
    fc = get_full_cut(p)
    return {p: 0.60, fc: 0.40}

def main():
    print("\n" + "="*80)
    print("  GRAND CROSS-VERSION EVALUATION — FRIDAY SINGLE OPEN PREDICTION")
    print("="*80)
    print(f"  Context: Thu Result = {YESTERDAY_JODI:02d} | Target = Friday")
    
    seq = load_full_sequence()
    print(f"  Total Historical Depth: {len(seq)} samples")
    
    versions = {
        "v16 (Genesis Pulse)": get_v16_logic(YESTERDAY_JODI),
        "v26 (Symmetry Oracle)": get_v26_logic(YESTERDAY_JODI),
        "v35 (Sequence GNN)": get_v35_logic(seq),
        "v40 (Ascension Hub)": get_v40_logic(seq)
    }
    
    # Synthesis
    grand_consensus = Counter()
    open_consensus = Counter()
    
    print("\n" + "-"*80)
    print(f"  {'VERSION':<25} | {'TOP JODI':<10} | {'PREDICTED OPEN':<15}")
    print("-" * 80)
    
    for name, logic in versions.items():
        best_jodi = max(logic.items(), key=lambda x: x[1])[0]
        pred_open = best_jodi // 10
        print(f"  {name:<25} | {best_jodi:02d}       | {pred_open:<15}")
        
        for jodi, weight in logic.items():
            grand_consensus[jodi] += weight
            open_consensus[jodi // 10] += weight

    # Final Weights
    total_jodi = sum(grand_consensus.values())
    total_open = sum(open_consensus.values())
    
    sorted_jodi = sorted(grand_consensus.items(), key=lambda x: x[1], reverse=True)
    sorted_open = sorted(open_consensus.items(), key=lambda x: x[1], reverse=True)
    
    print("\n" + "="*80)
    print("  FINAL SYNTHESIS RESULTS")
    print("="*80)
    
    print("\n  [TOP CONVERGENT OPEN DIGITS]:")
    for digit, score in sorted_open[:3]:
        print(f"    - Open {digit}: {(score/total_open)*100:.2f}% confidence")
        
    print("\n  [TOP CONVERGENT JODIS]:")
    for jodi, score in sorted_jodi[:3]:
        print(f"    - Jodi {jodi:02d}: {(score/total_jodi)*100:.2f}% confidence")
        
    print("\n" + "-"*80)
    print(f"  >>> PRIMARY SINGLE OPEN RECOMMENDATION: {sorted_open[0][0]}")
    print(f"  >>> SECONDARY (CUT) OPEN RECOMMENDATION: {sorted_open[1][0]}")
    print("-" * 80)
    print()

if __name__ == "__main__":
    main()
