"""
Predict TODAY's (Tuesday 31/03/2026) Jodi given yesterday's (Monday) Jodi = 74
Uses: ML model + Statistical ensemble + Cross-day MON->TUE transition analysis
"""

import sys, io, os, warnings
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV

warnings.filterwarnings('ignore')
# Standard logging and warnings
warnings.filterwarnings('ignore')

# --- CONFIG ---
YESTERDAY_JODI = 74       # Monday's actual Jodi
TODAY_DAY = "TUE"          # Predicting for Tuesday
YESTERDAY_DAY = "MON"

EXCEL_FILE_1 = "Number_Chart.xlsx"
EXCEL_FILE_2 = "Kalyan_Panel_Chart_Dataset.xlsx"
SHEET_NAME_1 = "Numeric Analysis"
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
WINDOW_SIZE = 15

# --- DATA LOADING ---
def load_data():
    per_day = {}
    # Source 1
    if os.path.exists(EXCEL_FILE_1):
        df = pd.read_excel(EXCEL_FILE_1, sheet_name=SHEET_NAME_1, header=0)
        for day in DAYS:
            col = f"{day} Jodi Num"
            if col in df.columns:
                vals = pd.to_numeric(df[col], errors="coerce").dropna().astype(int).tolist()
                per_day[day] = vals
    # Source 2 (supplement)
    if os.path.exists(EXCEL_FILE_2):
        df2 = pd.read_excel(EXCEL_FILE_2)
        cols = {c.strip().lower(): c for c in df2.columns}
        day_col = cols.get('day')
        jodi_col = cols.get('jodi')
        if day_col and jodi_col:
            if 'date' in cols:
                df2[cols['date']] = pd.to_datetime(df2[cols['date']], errors='coerce', dayfirst=True)
                df2 = df2.sort_values(by=cols['date'])
            for day in DAYS:
                mask = df2[day_col].astype(str).str.strip().str.upper().str.startswith(day)
                subset = df2[mask]
                vals2 = pd.to_numeric(subset[jodi_col], errors="coerce").dropna().astype(int)
                vals2 = vals2[(vals2 >= 0) & (vals2 <= 99)].tolist()
                if day not in per_day:
                    per_day[day] = vals2
                else:
                    # Use source 2 as backup (usually source 1 is more complete)
                    if len(vals2) > len(per_day.get(day, [])):
                        per_day[day] = vals2
    return per_day


# --- METHOD 1: ML MODEL (same as train_small_model.py) ---
def ml_predict(tue_seq):
    """Train RF+HGB ensemble on TUE history and predict next."""
    if len(tue_seq) < WINDOW_SIZE + 5:
        return None, []
    
    X, yt, yu = [], [], []
    for i in range(len(tue_seq) - WINDOW_SIZE):
        window = tue_seq[i:i+WINDOW_SIZE]
        target = tue_seq[i+WINDOW_SIZE]
        features = []
        for j, val in enumerate(window):
            tens = val // 10
            units = val % 10
            delta = 0 if j == 0 else (val - window[j-1])
            features.extend([tens, units, delta, tens % 2, units % 2])
        X.append(features)
        yt.append(target // 10)
        yu.append(target % 10)
    
    X = np.array(X)
    yt = np.array(yt)
    yu = np.array(yu)
    
    # Train tens model
    rf_t = RandomForestClassifier(n_estimators=150, max_depth=5, random_state=42, class_weight='balanced', n_jobs=-1)
    hgb_t = HistGradientBoostingClassifier(learning_rate=0.05, max_leaf_nodes=31, random_state=42)
    ens_t = VotingClassifier(estimators=[('rf', rf_t), ('hgb', hgb_t)], voting='soft')
    
    # Train units model
    rf_u = RandomForestClassifier(n_estimators=150, max_depth=5, random_state=42, class_weight='balanced', n_jobs=-1)
    hgb_u = HistGradientBoostingClassifier(learning_rate=0.05, max_leaf_nodes=31, random_state=42)
    ens_u = VotingClassifier(estimators=[('rf', rf_u), ('hgb', hgb_u)], voting='soft')
    
    ens_t.fit(X, yt)
    ens_u.fit(X, yu)
    
    # Predict using last window
    current_window = tue_seq[-WINDOW_SIZE:]
    features = []
    for j, val in enumerate(current_window):
        tens = val // 10
        units = val % 10
        delta = 0 if j == 0 else (val - current_window[j-1])
        features.extend([tens, units, delta, tens % 2, units % 2])
    
    X_pred = np.array([features])
    probs_t = ens_t.predict_proba(X_pred)[0]
    probs_u = ens_u.predict_proba(X_pred)[0]
    
    # Top 4 combinations
    classes_t = ens_t.classes_
    classes_u = ens_u.classes_
    
    jodi_probs = []
    for i, t in enumerate(classes_t):
        for j, u in enumerate(classes_u):
            prob = probs_t[i] * probs_u[j]
            jodi_probs.append((int(t) * 10 + int(u), prob))
    
    jodi_probs.sort(key=lambda x: x[1], reverse=True)
    return jodi_probs[0][0], jodi_probs[:6]


# --- METHOD 2: CROSS-DAY TRANSITION (MON -> TUE) ---
def cross_day_predict(mon_vals, tue_vals, yesterday_jodi):
    """Analyse what TUE Jodi typically follows a given MON Jodi."""
    min_len = min(len(mon_vals), len(tue_vals))
    if min_len < 5:
        return None, []
    
    # Find all times MON had same tens digit as yesterday
    yesterday_tens = yesterday_jodi // 10
    yesterday_units = yesterday_jodi % 10
    
    # Exact match transitions
    exact_followers = []
    tens_followers = []
    units_followers = []
    delta_list = []
    
    for i in range(min_len):
        delta_list.append(tue_vals[i] - mon_vals[i])
        if mon_vals[i] == yesterday_jodi:
            exact_followers.append(tue_vals[i])
        if mon_vals[i] // 10 == yesterday_tens:
            tens_followers.append(tue_vals[i])
        if mon_vals[i] % 10 == yesterday_units:
            units_followers.append(tue_vals[i])
    
    results = []
    
    # When MON was exactly the same
    if exact_followers:
        c = Counter(exact_followers)
        best = c.most_common(1)[0][0]
        results.append({
            "method": f"After MON={yesterday_jodi:02d} exactly",
            "prediction": best,
            "confidence": 0.50,
            "detail": f"Happened {len(exact_followers)} times, TUE was: {exact_followers}"
        })
    
    # When MON had same tens digit
    if tens_followers:
        c = Counter(tens_followers)
        best = c.most_common(1)[0][0]
        results.append({
            "method": f"After MON tens={yesterday_tens}",
            "prediction": best,
            "confidence": 0.25,
            "detail": f"{len(tens_followers)} matches"
        })
    
    # When MON had same units digit
    if units_followers:
        c = Counter(units_followers)
        best = c.most_common(1)[0][0]
        results.append({
            "method": f"After MON units={yesterday_units}",
            "prediction": best,
            "confidence": 0.25,
            "detail": f"{len(units_followers)} matches"
        })
    
    # Delta-based (average MON->TUE change applied to yesterday)
    avg_delta = np.mean(delta_list)
    median_delta = np.median(delta_list)
    pred_avg = (yesterday_jodi + int(round(avg_delta))) % 100
    pred_med = (yesterday_jodi + int(round(median_delta))) % 100
    if pred_avg < 0: pred_avg += 100
    if pred_med < 0: pred_med += 100
    
    results.append({
        "method": f"MON->TUE avg delta ({avg_delta:+.1f})",
        "prediction": pred_avg,
        "confidence": 0.20,
        "detail": f"74 + {avg_delta:.1f} ? {pred_avg:02d}"
    })
    
    # Recent delta (last 5 weeks only)
    recent_delta = delta_list[-5:]
    avg_recent = np.mean(recent_delta)
    pred_recent = (yesterday_jodi + int(round(avg_recent))) % 100
    if pred_recent < 0: pred_recent += 100
    results.append({
        "method": f"MON->TUE recent delta ({avg_recent:+.1f})",
        "prediction": pred_recent,
        "confidence": 0.30,
        "detail": f"Last 5 deltas: {recent_delta}"
    })
    
    return results[0]["prediction"] if results else None, results


# --- METHOD 3: TUESDAY STATISTICAL PATTERNS ---
def stat_predict(tue_vals):
    """Pure TUE-day statistical analysis."""
    results = []
    
    if len(tue_vals) < 5:
        return None, []
    
    # Frequency (recent 20)
    recent_20 = tue_vals[-20:]
    c20 = Counter(recent_20)
    top3 = c20.most_common(3)
    results.append({
        "method": "TUE frequency (recent 20)",
        "prediction": top3[0][0],
        "confidence": top3[0][1] / len(recent_20),
        "detail": f"Top: {[(f'{v:02d}', cnt) for v, cnt in top3]}"
    })
    
    # Weighted Moving Average + trend
    recent_5 = tue_vals[-5:]
    weights = [1, 2, 3, 4, 5]
    wma = sum(v * w for v, w in zip(recent_5, weights)) / sum(weights)
    diffs = [tue_vals[i+1] - tue_vals[i] for i in range(len(tue_vals)-1)]
    recent_diffs = diffs[-10:]
    trend = np.mean(recent_diffs)
    pred_wma = int(round(wma + trend)) % 100
    if pred_wma < 0: pred_wma += 100
    results.append({
        "method": "TUE WMA + trend",
        "prediction": pred_wma,
        "confidence": 0.25,
        "detail": f"WMA={wma:.1f}, trend={trend:.1f}"
    })
    
    # Modular digit analysis
    tens_recent = Counter(v // 10 for v in recent_20)
    units_recent = Counter(v % 10 for v in recent_20)
    t = tens_recent.most_common(1)[0][0]
    u = units_recent.most_common(1)[0][0]
    results.append({
        "method": "TUE modular (top tens+units)",
        "prediction": t * 10 + u,
        "confidence": 0.20,
        "detail": f"Tens={tens_recent.most_common(3)}, Units={units_recent.most_common(3)}"
    })
    
    # Difference extrapolation
    last_diff = diffs[-1]
    pred_diff = (tue_vals[-1] + last_diff) % 100
    if pred_diff < 0: pred_diff += 100
    results.append({
        "method": "TUE diff extrapolation",
        "prediction": pred_diff,
        "confidence": 0.15,
        "detail": f"Last diff={last_diff}, {tue_vals[-1]:02d} + {last_diff} = {pred_diff:02d}"
    })
    
    # Overdue numbers (not seen for long)
    last_seen = {}
    for i, v in enumerate(tue_vals):
        last_seen[v] = i
    current_idx = len(tue_vals) - 1
    gaps = {v: current_idx - idx for v, idx in last_seen.items()}
    overdue = sorted(gaps.items(), key=lambda x: -x[1])[:5]
    if overdue:
        results.append({
            "method": "TUE overdue number",
            "prediction": overdue[0][0],
            "confidence": 0.10,
            "detail": f"Overdue: {[(f'{v:02d}', g) for v, g in overdue[:5]]}"
        })
    
    return results[0]["prediction"] if results else None, results


# --- ENSEMBLE ---
def ensemble_all(all_preds):
    """Weighted vote across all methods."""
    votes = {}
    for p in all_preds:
        pred = p.get("prediction")
        if pred is not None:
            conf = p.get("confidence", 0.1)
            votes[pred] = votes.get(pred, 0.0) + conf
    
    if not votes:
        return 50, 0.0, []
    
    sorted_votes = sorted(votes.items(), key=lambda x: -x[1])
    total = sum(votes.values())
    
    top4 = [(v, round(w/total, 3)) for v, w in sorted_votes[:4]]
    return top4[0][0], top4[0][1], top4


# --- SWARM INTEGRATION ---
def get_swarm_results(today_day, yesterday_jodi):
    """Call the new swarm_predictor.py and format for this script."""
    try:
        from swarm_predictor import run_swarm
        swarm_preds = run_swarm(target_day=today_day, yesterday_jodi=yesterday_jodi)
        results = []
        for jodi, confidence in swarm_preds:
            results.append({
                "method": "Swarm Engine",
                "prediction": jodi,
                "confidence": confidence * 1.5, # Boost swarm weight
            })
        return results
    except Exception as e:
        print("  ! Could not run swarm_predictor: " + str(e))
        return []


# =======================================
# MAIN
# =======================================
def main():
    print()
    print("=" * 65)
    print(f"  TODAY'S JODI PREDICTION ? {TODAY_DAY} 31/03/2026")
    print(f"  Yesterday (MON) Jodi = {YESTERDAY_JODI:02d}")
    print("=" * 65)
    print()
    
    data = load_data()
    
    mon_vals = data.get("MON", [])
    tue_vals = data.get("TUE", [])
    
    print(f"  MON history: {len(mon_vals)} values | Last 5: {', '.join(f'{v:02d}' for v in mon_vals[-5:])}")
    print(f"  TUE history: {len(tue_vals)} values | Last 5: {', '.join(f'{v:02d}' for v in tue_vals[-5:])}")
    print()
    
    all_predictions = []
    
    # -- Swarm Engine (MiroFish Inspired) --
    print("-" * 65)
    print("  MIRORFISH-INSPIRED SWARM ENGINE")
    print("-" * 65)
    swarm_results = get_swarm_results(TODAY_DAY, YESTERDAY_JODI)
    all_predictions.extend(swarm_results)
    if swarm_results:
        top_swarm = swarm_results[0]
        print(f"    [Swarm Primary Prediction] ? {top_swarm['prediction']:02d}")
    print()

    # -- Method 1: ML Model --
    print("-" * 65)
    print("  METHOD 1: ML MODEL (Random Forest + Hist Gradient Boosting)")
    print("-" * 65)
    ml_best, ml_top = ml_predict(tue_vals)
    if ml_top:
        for idx, (jodi, prob) in enumerate(ml_top[:4]):
            tag = "*" if idx == 0 else " "
            print(f"    {tag} #{idx+1}: {jodi:02d}  (probability: {prob*100:.2f}%)")
            all_predictions.append({
                "method": f"ML Model #{idx+1}",
                "prediction": jodi,
                "confidence": prob * 2,  # scale up for voting weight
            })
    else:
        print("    ! Not enough data for ML model")
    print()
    
    # -- Method 2: Cross-Day Transition --
    print("-" * 65)
    print(f"  METHOD 2: CROSS-DAY TRANSITION (MON {YESTERDAY_JODI:02d} ? TUE ?)")
    print("-" * 65)
    _, cross_results = cross_day_predict(mon_vals, tue_vals, YESTERDAY_JODI)
    for r in cross_results:
        print(f"    [{r['method']:40s}] ? {r['prediction']:02d}  (conf {r['confidence']:.0%})")
        if r.get('detail'):
            print(f"      Detail: {r['detail']}")
        all_predictions.append(r)
    print()
    
    # -- Method 3: TUE Statistical Patterns --
    print("-" * 65)
    print("  METHOD 3: TUESDAY STATISTICAL PATTERNS")
    print("-" * 65)
    _, stat_results = stat_predict(tue_vals)
    for r in stat_results:
        print(f"    [{r['method']:40s}] ? {r['prediction']:02d}  (conf {r['confidence']:.0%})")
        if r.get('detail'):
            print(f"      Detail: {r['detail']}")
        all_predictions.append(r)
    print()
    
    # -- FINAL ENSEMBLE --
    best, conf, top4 = ensemble_all(all_predictions)
    
    print("=" * 65)
    print("  *** FINAL ENSEMBLE PREDICTION FOR " + TODAY_DAY + " 31/03/2026 ***")
    print("=" * 65)
    print()
    for idx, (jodi, weight) in enumerate(top4):
        rank = ["1st", "2nd", "3rd", "4th"][idx]
        marker = "  >>>  " if idx == 0 else "       "
        print(f"  {marker}{rank} Choice:  {jodi:02d}   (weight: {weight:.0%})")
    print()
    print(f"  Yesterday MON = {YESTERDAY_JODI:02d}")
    print(f"  Today {TODAY_DAY} prediction = {top4[0][0]:02d} (primary)")
    print()
    print("=" * 65)
    print()


if __name__ == "__main__":
    main()
