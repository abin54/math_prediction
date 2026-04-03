"""
Predict WEDNESDAY (01/04/2026) Jodi given Tuesday's Jodi = 04
Uses: ML model + Statistical ensemble + Cross-day TUE->WED transition analysis
"""

import sys, io, os, warnings
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier, VotingClassifier

warnings.filterwarnings('ignore')

# --- CONFIG ---
YESTERDAY_JODI = 4         # Tuesday's actual Jodi
TODAY_DAY = "WED"          # Predicting for Wednesday
YESTERDAY_DAY = "TUE"

EXCEL_FILE_1 = "Number_Chart.xlsx"
EXCEL_FILE_2 = "Kalyan_Panel_Chart_Dataset.xlsx"
SHEET_NAME_1 = "Numeric Analysis"
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
WINDOW_SIZE = 15

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
    if os.path.exists(EXCEL_FILE_2):
        df2 = pd.read_excel(EXCEL_FILE_2)
        cols = {c.strip().lower(): c for c in df2.columns}
        day_col = cols.get('day')
        jodi_col = cols.get('jodi')
        if day_col and jodi_col:
            for day in DAYS:
                mask = df2[day_col].astype(str).str.strip().str.upper().str.startswith(day)
                subset = df2[mask]
                vals2 = pd.to_numeric(subset[jodi_col], errors="coerce").dropna().astype(int)
                vals2 = vals2[(vals2 >= 0) & (vals2 <= 99)].tolist()
                if day not in per_day:
                    per_day[day] = vals2
                else:
                    if len(vals2) > len(per_day.get(day, [])):
                        per_day[day] = vals2
    return per_day

# --- METHOD 1: ML MODEL ---
def ml_predict(target_seq):
    if len(target_seq) < WINDOW_SIZE + 5:
        return None, []
    X, yt, yu = [], [], []
    for i in range(len(target_seq) - WINDOW_SIZE):
        window = target_seq[i:i+WINDOW_SIZE]
        target = target_seq[i+WINDOW_SIZE]
        features = []
        for j, val in enumerate(window):
            tens, units = val // 10, val % 10
            delta = 0 if j == 0 else (val - window[j-1])
            features.extend([tens, units, delta, tens % 2, units % 2])
        X.append(features)
        yt.append(target // 10)
        yu.append(target % 10)
    
    ens_t = VotingClassifier(estimators=[
        ('rf', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)),
        ('hgb', HistGradientBoostingClassifier(random_state=42))], voting='soft')
    ens_u = VotingClassifier(estimators=[
        ('rf', RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)),
        ('hgb', HistGradientBoostingClassifier(random_state=42))], voting='soft')
    
    ens_t.fit(X, yt)
    ens_u.fit(X, yu)
    
    current_window = target_seq[-WINDOW_SIZE:]
    features = []
    for j, val in enumerate(current_window):
        tens, units = val // 10, val % 10
        delta = 0 if j == 0 else (val - current_window[j-1])
        features.extend([tens, units, delta, tens % 2, units % 2])
    
    probs_t = ens_t.predict_proba([features])[0]
    probs_u = ens_u.predict_proba([features])[0]
    
    jodi_probs = []
    for i, t in enumerate(ens_t.classes_):
        for j, u in enumerate(ens_u.classes_):
            jodi_probs.append((int(t)*10 + int(u), probs_t[i] * probs_u[j]))
    
    jodi_probs.sort(key=lambda x: x[1], reverse=True)
    return jodi_probs[0][0], jodi_probs[:6]

# --- METHOD 2: CROSS-DAY (TUE -> WED) ---
def cross_day_predict(tue_vals, wed_vals, yesterday_jodi):
    min_len = min(len(tue_vals), len(wed_vals))
    results = []
    
    exact_match = [wed_vals[i] for i in range(min_len) if tue_vals[i] == yesterday_jodi]
    if exact_match:
        best = Counter(exact_match).most_common(1)[0][0]
        results.append({"method": "Exact TUE->WED Match", "prediction": best, "confidence": 0.4})
        
    # Delta Logic
    deltas = [wed_vals[i] - tue_vals[i] for i in range(min_len)]
    avg_delta = int(round(np.mean(deltas)))
    results.append({"method": "Avg Delta", "prediction": (yesterday_jodi + avg_delta) % 100, "confidence": 0.2})
    
    return results

# --- MAIN ---
def main():
    data = load_data()
    wed_vals = data.get("WED", [])
    tue_vals = data.get("TUE", [])
    
    print("\n--- ML PREDICTIONS (WED) ---")
    best_ml, top_ml = ml_predict(wed_vals)
    for j, p in top_ml[:4]:
        print(f"Jodi: {j:02d} (Prob: {p:.2%})")
        
    print("\n--- CROSS-DAY PREDICTIONS (TUE 04 -> WED ?) ---")
    cross = cross_day_predict(tue_vals, wed_vals, YESTERDAY_JODI)
    for r in cross:
        print(f"{r['method']}: {r['prediction']:02d}")

if __name__ == "__main__":
    main()
