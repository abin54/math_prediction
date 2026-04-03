"""
Deep Logic Archiver v1.0 — Matka Chart DNA Tagger
=================================================
Analyzes the entire 10-year history and "Tags" every transition 
with the specific Matka Trick that caused it. 
"""

import pandas as pd
import numpy as np
import os
from collections import Counter

# CONFIG
CHART_FILE = "Number_Chart.xlsx"
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
MIRROR = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}

def get_total(v):
    try:
        v = int(pd.to_numeric(v, errors='coerce'))
        return (v // 10 + v % 10) % 10
    except:
        return -1

def get_family(n):
    t, u = n // 10, n % 10
    mt, mu = MIRROR[t], MIRROR[u]
    return {t*10+u, t*10+mu, mt*10+u, mt*10+mu, u*10+t, u*10+mt, mu*10+t, mu*10+mt}

def tag_transition(v1, v2):
    """Identify which 'Trick' connects v1 to v2."""
    if pd.isna(v1) or pd.isna(v2): return "NONE"
    
    v1, v2 = int(v1), int(v2)
    t1, u1 = v1 // 10, v1 % 10
    t2, u2 = v2 // 10, v2 % 10
    tot1, tot2 = get_total(v1), get_total(v2)
    
    tags = []
    
    # 1. Mirror/Cut Trick
    if t2 == MIRROR[t1] or t2 == MIRROR[u1] or u2 == MIRROR[t1] or u2 == MIRROR[u1]:
        tags.append("MIRROR")
        
    # 2. Step Logic (+3 / +7 / +1)
    if (tot1 + 3) % 10 == tot2: tags.append("STEP-3")
    if (tot1 + 7) % 10 == tot2: tags.append("STEP-7")
    if (tot1 + 1) % 10 == tot2: tags.append("STEP-1")
    
    # 3. Digit Repetition (Unit/Tens Lock)
    if u1 == u2: tags.append("UNIT-LOCK")
    if t1 == t2: tags.append("TENS-LOCK")
    
    # 4. Family Continuity
    if v2 in get_family(v1):
        tags.append("FAMILY")
        
    # 5. Mirror Symmetry (Total 1<->6, 4<->9)
    # If tot1 is 1 and tot2 is 4, it's our current "Step-3"
    # If tot1 is 6 and tot2 is 9, it's the "Mirror of Step-3"
    if (tot1 == 1 and tot2 == 4) or (tot1 == 6 and tot2 == 9):
        tags.append("STEP-3-SYM")
        
    return "|".join(tags) if tags else "UNKNOWN"

def run_archiver():
    if not os.path.exists(CHART_FILE):
        print("Chart not found.")
        return
        
    df = pd.read_excel(CHART_FILE, sheet_name="Numeric Analysis")
    
    all_tags = Counter()
    history_log = []
    
    # Track all day-to-day transitions
    for idx, row in df.iterrows():
        week_tags = []
        for i in range(len(DAYS) - 1):
            d1, d2 = DAYS[i], DAYS[i+1]
            v1, v2 = row[f"{d1} Jodi Num"], row[f"{d2} Jodi Num"]
            tag = tag_transition(v1, v2)
            if tag != "NONE":
                week_tags.append(f"{d1}->{d2}:{tag}")
                for t in tag.split("|"):
                    all_tags[t] += 1
        
        history_log.append({
            "Week": row["Date Range"],
            "Trace": " ".join(week_tags)
        })
        
    # Stats
    print("\n" + "="*60)
    print("  MATKA CHART LOGIC AUDIT — DNA FREQUENCY")
    print("="*60)
    total_samples = sum(all_tags.values())
    for tag, count in all_tags.most_common():
        pct = (count / total_samples) * 100
        print(f"  {tag:15}: {count:4} occurrences ({pct:.1f}%)")
    print("="*60)
    
    # Save a sample of the Trace Log
    with open("historical_logic_trace.txt", "w") as f:
        f.write("HISTORICAL TRICK TRACE LOG\n")
        f.write("==========================\n\n")
        for log in history_log[-20:]: # Last 20 weeks
            f.write(f"Week: {log['Week'].replace('\\n', ' ')}\n")
            f.write(f"Logic Trace: {log['Trace']}\n")
            f.write("-" * 50 + "\n")

if __name__ == "__main__":
    run_archiver()
