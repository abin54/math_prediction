"""
Predict TODAY's (Thursday 02/04/2026) Jodi given yesterday's (Wednesday) Jodi = 19
Uses: ML model + Statistical ensemble + Cross-day WED->THU transition analysis
"""

import sys, io, os, warnings
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV

warnings.filterwarnings('ignore')

# --- CONFIG ---
YESTERDAY_JODI = 19       # Wednesday's actual Jodi
TODAY_DAY = "THU"          # Predicting for Thursday
YESTERDAY_DAY = "WED"

EXCEL_FILE_1 = "Number_Chart.xlsx"
EXCEL_FILE_2 = "Kalyan_Panel_Chart_Dataset.xlsx"
SHEET_NAME_1 = "Numeric Analysis"
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
WINDOW_SIZE = 12

# --- DATA LOADING ---
def load_data():
    per_day = {}
    if os.path.exists(EXCEL_FILE_1):
        df = pd.read_excel(EXCEL_FILE_1, sheet_name=SHEET_NAME_1, header=0)
        for day in DAYS:
            col = f"{day} Jodi Num"
            if col in df.columns:
                vals = pd.to_numeric(df[col], errors="coerce").dropna().astype(int).tolist()
                per_day[day] = vals
    return per_day

def ml_predict(target_seq):
    if len(target_seq) < WINDOW_SIZE + 5:
        return None, []
    X, yt, yu = [], [], []
    for i in range(len(target_seq) - WINDOW_SIZE):
        window = target_seq[i:i+WINDOW_SIZE]
        target = target_seq[i+WINDOW_SIZE]
        features = []
        for j, val in enumerate(window):
            tens = val // 10
            units = val % 10
            delta = 0 if j == 0 else (val - window[j-1])
            features.extend([tens, units, delta])
        X.append(features)
        yt.append(target // 10)
        yu.append(target % 10)
    
    rf_t = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf_u = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rf_t.fit(X, yt)
    rf_u.fit(X, yu)
    
    current_window = target_seq[-WINDOW_SIZE:]
    features = []
    for j, val in enumerate(current_window):
        features.extend([val // 10, val % 10, 0 if j == 0 else (val - current_window[j-1])])
    
    probs_t = rf_t.predict_proba([features])[0]
    probs_u = rf_u.predict_proba([features])[0]
    
    jodi_probs = []
    for i, t in enumerate(rf_t.classes_):
        for j, u in enumerate(rf_u.classes_):
            jodi_probs.append((int(t) * 10 + int(u), probs_t[i] * probs_u[j]))
    jodi_probs.sort(key=lambda x: x[1], reverse=True)
    return jodi_probs[0][0], jodi_probs[:6]

def cross_day_predict(prev_vals, target_vals, yesterday_jodi):
    min_len = min(len(prev_vals), len(target_vals))
    exact_followers = []
    for i in range(min_len):
        if prev_vals[i] == yesterday_jodi:
            exact_followers.append(target_vals[i])
    
    results = []
    if exact_followers:
        c = Counter(exact_followers)
        results.append({"method": "Exact Transition", "prediction": c.most_common(1)[0][0], "confidence": 0.4})
    
    # Delta
    deltas = [target_vals[i] - prev_vals[i] for i in range(min_len)]
    avg_delta = int(round(np.mean(deltas[-10:])))
    pred_delta = (yesterday_jodi + avg_delta) % 100
    results.append({"method": "Avg Delta", "prediction": pred_delta, "confidence": 0.2})
    
    return results

def main():
    data = load_data()
    prev_vals = data.get(YESTERDAY_DAY, [])
    target_vals = data.get(TODAY_DAY, [])
    
    print(f"Analyzing {YESTERDAY_DAY} ({YESTERDAY_JODI}) -> {TODAY_DAY} pattern...")
    
    ml_best, ml_top = ml_predict(target_vals)
    cross_results = cross_day_predict(prev_vals, target_vals, YESTERDAY_JODI)
    
    print("\n[ML Results] Top 3:")
    for j, p in ml_top[:3]:
        print(f" - {j:02d} ({p:.1%})")
        
    print("\n[Transition Results]:")
    for r in cross_results:
        print(f" - {r['method']}: {r['prediction']:02d}")

if __name__ == "__main__":
    main()
