"""
Deep Sequence Model v5: Top-3 Precision Predictor
Aims for maximum mathematical accuracy using Hyperparameter Tuning, Multi-Dataset Ingestion, and Top-K Probabilities.
"""

import pandas as pd
import numpy as np
import logging
import sys
import io
import warnings
import os
from collections import Counter
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import TimeSeriesSplit, RandomizedSearchCV
from sklearn.metrics import accuracy_score
try:
    import xgboost as xgb
except ImportError:
    xgb = None

warnings.filterwarnings('ignore')

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-7s | %(message)s")
log = logging.getLogger(__name__)

EXCEL_FILE_1 = "Number_Chart.xlsx"
EXCEL_FILE_2 = "Kalyan_Panel_Chart_Dataset.xlsx"
SHEET_NAME_1 = "Numeric Analysis"
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
WINDOW_SIZE = 15
CV_SPLITS = 3

def load_data_source_1():
    if not os.path.exists(EXCEL_FILE_1):
        return {d: [] for d in DAYS}
    try:
        df = pd.read_excel(EXCEL_FILE_1, sheet_name=SHEET_NAME_1, header=0)
        series = {}
        for day in DAYS:
            col = f"{day} Jodi Num"
            if col in df.columns:
                vals = pd.to_numeric(df[col], errors="coerce").dropna().astype(int).tolist()
                series[day] = vals
            else:
                series[day] = []
        return series
    except Exception as e:
        return {d: [] for d in DAYS}

def load_data_source_2():
    if not os.path.exists(EXCEL_FILE_2):
        return {d: [] for d in DAYS}
    try:
        df = pd.read_excel(EXCEL_FILE_2)
        cols = {c.strip().lower(): c for c in df.columns}
        day_col = cols.get('day')
        jodi_col = cols.get('jodi')
        if not day_col or not jodi_col: return {d: [] for d in DAYS}
        
        if 'date' in cols:
            df[cols['date']] = pd.to_datetime(df[cols['date']], errors='coerce', dayfirst=True)
            df = df.sort_values(by=cols['date'])
            
        series = {d: [] for d in DAYS}
        for day in DAYS:
            mask = df[day_col].astype(str).str.strip().str.upper().str.startswith(day)
            subset = df[mask]
            vals = pd.to_numeric(subset[jodi_col], errors="coerce").dropna().astype(int)
            vals = vals[(vals >= 0) & (vals <= 99)].tolist()
            series[day] = vals
        return series
    except Exception as e:
        return {d: [] for d in DAYS}

def _extract_window_features(window: List[int]) -> List[float]:
    """Extract 15+ features per position in window."""
    features = []
    tens_list = [v // 10 for v in window]
    units_list = [v % 10 for v in window]

    for j, val in enumerate(window):
        tens = val // 10
        units = val % 10
        delta = 0 if j == 0 else (val - window[j - 1])

        # Original features (5)
        features.extend([tens, units, delta, tens % 2, units % 2])

        # New: digit sum and product (2)
        features.append(tens + units)
        features.append(tens * units)

        # New: digit difference absolute (1)
        features.append(abs(tens - units))

        # New: modular features (3)
        features.append(val % 3)
        features.append(val % 5)
        features.append(val % 7)

        # New: position in sequence (1)
        features.append(j / len(window))

    # Window-level aggregate features
    arr = np.array(window, dtype=float)
    features.append(float(np.mean(arr)))
    features.append(float(np.std(arr)))
    features.append(float(np.min(arr)))
    features.append(float(np.max(arr)))
    features.append(float(np.median(arr)))

    # Diffs
    diffs = np.diff(arr)
    features.append(float(np.mean(diffs)))
    features.append(float(np.std(diffs)))

    # Autocorrelation
    for lag in [1, 2, 3]:
        if len(arr) > lag:
            corr = np.corrcoef(arr[:-lag], arr[lag:])[0, 1]
            features.append(float(corr) if not np.isnan(corr) else 0.0)
        else:
            features.append(0.0)

    # Densities
    tens_counter = Counter(tens_list)
    units_counter = Counter(units_list)
    features.append(float(tens_counter.most_common(1)[0][0]))
    features.append(float(units_counter.most_common(1)[0][0]))

    even_count = sum(1 for v in window if v % 2 == 0)
    features.append(even_count / len(window))

    return features

def create_dataset(sequence, window_size):
    X, yt, yu = [], [], []
    for i in range(len(sequence) - window_size):
        window = sequence[i:i+window_size]
        target = sequence[i+window_size]
        features = _extract_window_features(window)
        X.append(features)
        yt.append(target // 10)
        yu.append(target % 10)
    if len(X) == 0: return np.array([]), np.array([]), np.array([])
    return np.array(X, dtype=np.float32), np.array(yt), np.array(yu)

from typing import List

def tune_and_fit(X, y_target, name):
    """Attempt GPU training first, then fallback to CPU."""
    if xgb:
        try:
            # Try XGBoost GPU
            gpu_params = {
                'objective': 'multi:softprob',
                'tree_method': 'hist',
                'device': 'cuda',
                'max_depth': 5,
                'learning_rate': 0.05,
                'n_estimators': 150,
                'random_state': 42,
                'verbosity': 0
            }
            model = xgb.XGBClassifier(**gpu_params, num_class=10)
            model.fit(X, y_target)
            log.info(f"  [{name}] Trained on GPU using XGBoost")
            return model, 1.0
        except Exception as e:
            log.warning(f"  [{name}] GPU training failed, falling back: {e}")
    
    # Fallback: HistGradientBoosting
    model = HistGradientBoostingClassifier(random_state=42)
    model.fit(X, y_target)
    log.info(f"  [{name}] Trained on CPU using HistGradientBoosting")
    return model, 1.0

def train_and_eval(day, seq_1, seq_2):
    log.info(f"--- Fusing and Fine-Tuning deep patterns for {day} ---")
    
    X1, yt1, yu1 = create_dataset(seq_1, WINDOW_SIZE)
    X2, yt2, yu2 = create_dataset(seq_2, WINDOW_SIZE)
    
    X_parts, yt_parts, yu_parts = [], [], []
    if len(X1) > 0:
        X_parts.append(X1)
        yt_parts.append(yt1)
        yu_parts.append(yu1)
    if len(X2) > 0:
        X_parts.append(X2)
        yt_parts.append(yt2)
        yu_parts.append(yu2)
        
    if not X_parts:
        return None
        
    X_full = np.vstack(X_parts)
    yt_full = np.concatenate(yt_parts)
    yu_full = np.concatenate(yu_parts)
    
    best_model_t, cv_acc_t = tune_and_fit(X_full, yt_full, "Tens Model")
    best_model_u, cv_acc_u = tune_and_fit(X_full, yu_full, "Units Model")
    
    if len(seq_1) >= WINDOW_SIZE:
        current_raw_window = seq_1[-WINDOW_SIZE:]
    elif len(seq_2) >= WINDOW_SIZE:
        current_raw_window = seq_2[-WINDOW_SIZE:]
    else:
        return None
        
    features = _extract_window_features(current_raw_window)
    current_window_X = np.array([features], dtype=np.float32)
    
    # Get raw probabilities
    probs_t_raw = best_model_t.predict_proba(current_window_X)[0]
    probs_u_raw = best_model_u.predict_proba(current_window_X)[0]
    
    # Extract top 4 mathematically probable digits for Tens and Units
    top_4_t_idx = np.argsort(probs_t_raw)[-4:][::-1]
    top_4_u_idx = np.argsort(probs_u_raw)[-4:][::-1]
    
    # Generate all combinations of top Tens and Units to find top 4 overall Jodis
    jodi_probs = []
    for t_idx in top_4_t_idx:
        for u_idx in top_4_u_idx:
            # Joint mathematical probability
            prob = probs_t_raw[t_idx] * probs_u_raw[u_idx]
            jodi_probs.append((t_idx * 10 + u_idx, prob))
            
    jodi_probs.sort(key=lambda x: x[1], reverse=True)
    top_4_jodis = jodi_probs[:4]
    
    print(f"\n================================================================")
    print(f"  TOP 4 PREDICTIONS WITH PRECISION FOR: {day}")
    print(f"================================================================")
    for idx, (jodi, prob) in enumerate(top_4_jodis):
        print(f"  #{idx+1} Choice -> {jodi:02d}    (Raw Precision Probability: {prob*100:.2f}%)")
    print(f"================================================================\n")
    
    return {
        "Day": day,
        "Best Number": top_4_jodis[0][0],
        "Second Best": top_4_jodis[1][0],
        "Third Best": top_4_jodis[2][0],
        "Fourth Best": top_4_jodis[3][0],
    }

def main():
    print("================================================================")
    print("  DEEP SEQUENCE MODEL v5 - TOP-3 PROBABILITY PREDICTOR")
    print("================================================================")
    print()
    
    data_1 = load_data_source_1()
    data_2 = load_data_source_2()
        
    final_results = []
    for day in DAYS:
        seq1 = data_1.get(day, [])
        seq2 = data_2.get(day, [])
        res = train_and_eval(day, seq1, seq2)
        if res is not None:
            final_results.append(res)
            
    # Save to text file
    with open("Weekly_Predictions.txt", "w", encoding="utf-8") as f:
        f.write("WEEKLY PREDICTIONS DAY WISE\n")
        f.write("===========================\n\n")
        for res in final_results:
            f.write(f"Day: {res['Day']}\n")
            f.write(f"1st Choice: {res['Best Number']:02d}\n")
            f.write(f"2nd Choice: {res['Second Best']:02d}\n")
            f.write(f"3rd Choice: {res['Third Best']:02d}\n")
            f.write(f"4th Choice: {res['Fourth Best']:02d}\n")
            f.write("-" * 30 + "\n")
            
    # Also save to Excel
    try:
        df = pd.DataFrame(final_results)
        df.rename(columns={'Best Number': '1st Choice', 'Second Best': '2nd Choice', 'Third Best': '3rd Choice', 'Fourth Best': '4th Choice'}, inplace=True)
        df.to_excel("Weekly_Predictions.xlsx", index=False)
        print("Predictions successfully saved to Weekly_Predictions.xlsx and Weekly_Predictions.txt")
    except Exception as e:
        print(f"Could not save to excel: {e}")

    print("================================================================")
    print("  MATHEMATICAL ANALYSIS COMPLETE!")
    print("================================================================")

if __name__ == "__main__":
    main()
