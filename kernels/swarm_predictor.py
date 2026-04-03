"""
Swarm Predictor v1.0 ? MiroFish-Inspired Multi-Agent Prediction Engine
=====================================================================
6 independent prediction agents with weighted ensemble voting:
  1. StatAgent      ? Frequency + recency analysis
  2. TrendAgent     ? WMA + momentum + trend extrapolation
  3. TransitionAgent? Cross-day (MON?TUE etc.) transition patterns
  4. CycleAgent     ? Modular cycles, overdue numbers, gap analysis
  5. MLAgent        ? XGBoost GPU with enhanced feature engineering
  6. LLMAgent       ? Ollama llama3.2:3b reasoning

Resources: RAM capped at 6GB, GPU via XGBoost gpu_hist (GTX 1650)
"""

import sys, io, os, warnings, json, time
import pandas as pd
import numpy as np
import psutil
from collections import Counter
from typing import Dict, List, Tuple, Optional

warnings.filterwarnings('ignore')
# Standard logging and warnings
warnings.filterwarnings('ignore')

# ===========================================================
# CONFIG
# ===========================================================
EXCEL_FILE_1 = "Number_Chart.xlsx"
EXCEL_FILE_2 = "Kalyan_Panel_Chart_Dataset.xlsx"
SHEET_NAME_1 = "Sheet1"
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]

OLLAMA_URL = "http://127.0.0.1:11434"
OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_TIMEOUT = 60   # seconds

RAM_LIMIT_GB = 6.0
WINDOW_SIZE = 15

# Agent weights (sum = 1.0)
# Agent weights (can be overwritten by optimized_weights.json)
DEFAULT_AGENT_WEIGHTS = {
    "StatAgent":       0.15,
    "TrendAgent":      0.10,
    "TransitionAgent": 0.10,
    "CycleAgent":      0.10,
    "MirrorTraceAgent": 0.15,
    "SeriesSpikeAgent": 0.15,  # NEW
    "StepAgent":        0.10,  # NEW
    "MLAgent":         0.10,
    "LLMAgent":        0.05,
}

def load_optimized_weights():
    if os.path.exists("optimized_weights.json"):
        try:
            with open("optimized_weights.json", "r") as f:
                weights = json.load(f)
                # RED TEAM: Enforce 5% Floor
                for k in weights:
                    weights[k] = max(0.05, weights[k])
                return weights
        except: pass
    return DEFAULT_AGENT_WEIGHTS

AGENT_WEIGHTS = load_optimized_weights()

def load_learned_tricks():
    if os.path.exists("learned_tricks.json"):
        try:
            with open("learned_tricks.json", "r") as f:
                return json.load(f)
        except: pass
    return {}

LEARNED_TRICKS = load_learned_tricks()

class HistoryAgent:
    name = "HistoryAgent"

    def predict(self, yesterday_jodi: int = None, **kwargs) -> List[Tuple[int, float]]:
        if yesterday_jodi is None or not LEARNED_TRICKS:
            return []
            
        candidates = Counter()
        p_t, p_u = yesterday_jodi // 10, yesterday_jodi % 10
        
        # Apply Mirror Trick Weights
        m_set = get_mirror_set(yesterday_jodi)
        for m in m_set:
            candidates[m] += LEARNED_TRICKS.get("Mirror/Family", 0.04) * 100
            
        # Apply Open-Step Weights
        for s in [1, 2, 8, 9]:
            step_name = f"Open-Step-{s}"
            if step_name in LEARNED_TRICKS:
                pred_t = (p_t + s) % 10
                # Weighted boost for common steps
                for i in range(10):
                    candidates[pred_t * 10 + i] += LEARNED_TRICKS[step_name] * 50
                    
        # Apply Repeat Weights
        for i in range(10):
            candidates[p_t * 10 + i] += LEARNED_TRICKS.get("Repeat-Open", 0.11) * 30
            candidates[i * 10 + p_u] += LEARNED_TRICKS.get("Repeat-Close", 0.09) * 30
            
        # Apply Sum-Total Echo
        sum_p = (p_t + p_u) % 10
        for i in range(10):
            candidates[sum_p * 10 + i] += LEARNED_TRICKS.get("Sum-Total-Echo", 0.18) * 20
            candidates[i * 10 + sum_p] += LEARNED_TRICKS.get("Sum-Total-Echo", 0.18) * 20

        total = sum(candidates.values()) or 1
        return [(v, round(w / total, 3)) for v, w in candidates.most_common(8)]

def load_learned_tricks():
    if os.path.exists("learned_tricks.json"):
        try:
            with open("learned_tricks.json", "r") as f:
                return json.load(f)
        except: pass
    return {}

LEARNED_TRICKS = load_learned_tricks()

class HistoryAgent:
    name = "HistoryAgent"

    def predict(self, yesterday_jodi: int = None, **kwargs) -> List[Tuple[int, float]]:
        if yesterday_jodi is None or not LEARNED_TRICKS:
            return []
            
        candidates = Counter()
        p_t, p_u = yesterday_jodi // 10, yesterday_jodi % 10
        
        # Apply Mirror Trick Weights
        m_set = get_mirror_set(yesterday_jodi)
        for m in m_set:
            candidates[m] += LEARNED_TRICKS.get("Mirror/Family", 0.04) * 100
            
        # Apply Open-Step Weights
        for s in [1, 2, 8, 9]:
            step_name = f"Open-Step-{s}"
            if step_name in LEARNED_TRICKS:
                pred_t = (p_t + s) % 10
                # Weighted boost for common steps
                for i in range(10):
                    candidates[pred_t * 10 + i] += LEARNED_TRICKS[step_name] * 50
                    
        # Apply Repeat Weights
        for i in range(10):
            candidates[p_t * 10 + i] += LEARNED_TRICKS.get("Repeat-Open", 0.11) * 30
            candidates[i * 10 + p_u] += LEARNED_TRICKS.get("Repeat-Close", 0.09) * 30
            
        # Apply Sum-Total Echo
        sum_p = (p_t + p_u) % 10
        for i in range(10):
            candidates[sum_p * 10 + i] += LEARNED_TRICKS.get("Sum-Total-Echo", 0.18) * 20
            candidates[i * 10 + sum_p] += LEARNED_TRICKS.get("Sum-Total-Echo", 0.18) * 20

        total = sum(candidates.values()) or 1
        return [(v, round(w / total, 3)) for v, w in candidates.most_common(8)]

# Mirror/Cut map: 0?5, 1?6, 2?7, 3?8, 4?9
MIRROR = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}



# ===========================================================
# RAM MONITOR
# ===========================================================
def check_ram(label=""):
    process = psutil.Process(os.getpid())
    mem_gb = process.memory_info().rss / (1024 ** 3)
    if mem_gb > RAM_LIMIT_GB:
        print(f"  [RAM WARNING] {label}: {mem_gb:.2f} GB (limit: {RAM_LIMIT_GB} GB)")
    return mem_gb


# ===========================================================
# DATA LOADING
# ===========================================================
def load_all_data() -> Dict[str, List[int]]:
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
            if 'date' in cols:
                df2[cols['date']] = pd.to_datetime(df2[cols['date']], errors='coerce', dayfirst=True)
                df2 = df2.sort_values(by=cols['date'])
            for day in DAYS:
                mask = df2[day_col].astype(str).str.strip().str.upper().str.startswith(day)
                subset = df2[mask]
                vals2 = pd.to_numeric(subset[jodi_col], errors="coerce").dropna().astype(int)
                vals2 = vals2[(vals2 >= 0) & (vals2 <= 99)].tolist()
                if day not in per_day or len(vals2) > len(per_day.get(day, [])):
                    per_day[day] = vals2
    return per_day


# ===========================================================
# ENHANCED FEATURE ENGINEERING (15+ features per step)
# ===========================================================
def build_enhanced_features(sequence: List[int], window_size: int = WINDOW_SIZE):
    """Build rich feature vectors for ML training."""
    X, yt, yu = [], [], []
    for i in range(len(sequence) - window_size):
        window = sequence[i:i + window_size]
        target = sequence[i + window_size]
        features = _extract_window_features(window)
        X.append(features)
        yt.append(target // 10)
        yu.append(target % 10)
    if not X:
        return np.array([]), np.array([]), np.array([])
    return np.array(X, dtype=np.float32), np.array(yt), np.array(yu)


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

        # New: position in sequence (1) ? normalized
        features.append(j / len(window))

    # Window-level aggregate features
    arr = np.array(window, dtype=float)
    features.append(float(np.mean(arr)))        # rolling mean
    features.append(float(np.std(arr)))          # rolling std
    features.append(float(np.min(arr)))          # rolling min
    features.append(float(np.max(arr)))          # rolling max
    features.append(float(np.median(arr)))       # rolling median

    # Diffs within window
    diffs = np.diff(arr)
    features.append(float(np.mean(diffs)))       # avg diff
    features.append(float(np.std(diffs)))        # diff volatility

    # Autocorrelation features (lag 1-3)
    for lag in [1, 2, 3]:
        if len(arr) > lag:
            corr = np.corrcoef(arr[:-lag], arr[lag:])[0, 1]
            features.append(float(corr) if not np.isnan(corr) else 0.0)
        else:
            features.append(0.0)

    # Tens and units distribution in window
    tens_counter = Counter(tens_list)
    units_counter = Counter(units_list)
    features.append(float(tens_counter.most_common(1)[0][0]))   # dominant tens
    features.append(float(units_counter.most_common(1)[0][0]))  # dominant units

    # Even/odd ratio in window
    even_count = sum(1 for v in window if v % 2 == 0)
    features.append(even_count / len(window))

    # Digit sum trend
    dsums = [v // 10 + v % 10 for v in window]
    dsum_diffs = np.diff(dsums)
    features.append(float(np.mean(dsum_diffs)) if len(dsum_diffs) > 0 else 0.0)

    # Last value features (for recency)
    features.append(float(window[-1]))
    features.append(float(window[-1] // 10))
    features.append(float(window[-1] % 10))

    return features


# ===========================================================
# AGENT 1: StatAgent ? Frequency + Recency
# ===========================================================
class StatAgent:
    name = "StatAgent"

    def predict(self, target_day_vals: List[int], **kwargs) -> List[Tuple[int, float]]:
        if len(target_day_vals) < 5:
            return []

        scores = Counter()

        # Recent 20 frequency
        recent_20 = target_day_vals[-20:]
        c20 = Counter(recent_20)
        for v, cnt in c20.most_common(10):
            scores[v] += cnt * 5

        # All-time frequency
        c_all = Counter(target_day_vals)
        for v, cnt in c_all.most_common(10):
            scores[v] += cnt

        # Recent 10 frequency (higher recency weight)
        recent_10 = target_day_vals[-10:]
        c10 = Counter(recent_10)
        for v, cnt in c10.most_common(5):
            scores[v] += cnt * 8

        # Digit-level frequency (recent 20)
        tens_freq = Counter(v // 10 for v in recent_20)
        units_freq = Counter(v % 10 for v in recent_20)
        top_tens = [t for t, _ in tens_freq.most_common(3)]
        top_units = [u for u, _ in units_freq.most_common(3)]
        for t in top_tens:
            for u in top_units:
                scores[t * 10 + u] += 3

        total = sum(scores.values()) or 1
        results = [(v, w / total) for v, w in scores.most_common(8)]
        return results


# ===========================================================
# AGENT 2: TrendAgent ? WMA + Momentum
# ===========================================================
class TrendAgent:
    name = "TrendAgent"

    def predict(self, target_day_vals: List[int], **kwargs) -> List[Tuple[int, float]]:
        if len(target_day_vals) < 10:
            return []

        candidates = Counter()

        # Weighted Moving Average
        recent_5 = target_day_vals[-5:]
        weights = [1, 2, 3, 4, 5]
        wma = sum(v * w for v, w in zip(recent_5, weights)) / sum(weights)

        # Trend (recent diffs)
        diffs = [target_day_vals[i + 1] - target_day_vals[i]
                 for i in range(len(target_day_vals) - 1)]
        recent_diffs = diffs[-10:]
        trend = np.mean(recent_diffs)

        # WMA + trend prediction
        pred1 = int(round(wma + trend)) % 100
        if pred1 < 0: pred1 += 100
        candidates[pred1] += 10

        # Momentum (acceleration)
        if len(diffs) >= 5:
            accel = np.mean(diffs[-5:]) - np.mean(diffs[-10:-5]) if len(diffs) >= 10 else 0
            pred2 = int(round(wma + trend + accel)) % 100
            if pred2 < 0: pred2 += 100
            candidates[pred2] += 7

        # Exponential Moving Average
        alpha = 0.3
        ema = target_day_vals[-1]
        for v in reversed(target_day_vals[-10:]):
            ema = alpha * v + (1 - alpha) * ema
        pred3 = int(round(ema + trend)) % 100
        if pred3 < 0: pred3 += 100
        candidates[pred3] += 8

        # Diff extrapolation (last diff repeated)
        last_diff = diffs[-1] if diffs else 0
        pred4 = (target_day_vals[-1] + last_diff) % 100
        if pred4 < 0: pred4 += 100
        candidates[pred4] += 5

        # Median diff prediction
        med_diff = int(round(np.median(recent_diffs)))
        pred5 = (target_day_vals[-1] + med_diff) % 100
        if pred5 < 0: pred5 += 100
        candidates[pred5] += 5

        total = sum(candidates.values()) or 1
        return [(v, w / total) for v, w in candidates.most_common(6)]


# ===========================================================
# AGENT 3: TransitionAgent ? Cross-Day Patterns
# ===========================================================
class TransitionAgent:
    name = "TransitionAgent"

    def predict(self, target_day_vals: List[int], yesterday_vals: List[int] = None,
                yesterday_jodi: int = None, **kwargs) -> List[Tuple[int, float]]:
        if yesterday_vals is None or yesterday_jodi is None:
            return []

        min_len = min(len(yesterday_vals), len(target_day_vals))
        if min_len < 5:
            return []

        y_tens = yesterday_jodi // 10
        y_units = yesterday_jodi % 10
        candidates = Counter()

        exact_followers = []
        tens_followers = []
        units_followers = []
        all_deltas = []

        for i in range(min_len):
            all_deltas.append(target_day_vals[i] - yesterday_vals[i])
            if yesterday_vals[i] == yesterday_jodi:
                exact_followers.append(target_day_vals[i])
            if yesterday_vals[i] // 10 == y_tens:
                tens_followers.append(target_day_vals[i])
            if yesterday_vals[i] % 10 == y_units:
                units_followers.append(target_day_vals[i])

        # Exact match followers (strongest signal)
        for v in exact_followers:
            candidates[v] += 15

        # Tens match followers
        c_tens = Counter(tens_followers)
        for v, cnt in c_tens.most_common(5):
            candidates[v] += cnt * 3

        # Units match followers
        c_units = Counter(units_followers)
        for v, cnt in c_units.most_common(5):
            candidates[v] += cnt * 2

        # Delta-based predictions
        if all_deltas:
            avg_delta = np.mean(all_deltas)
            pred_avg = (yesterday_jodi + int(round(avg_delta))) % 100
            if pred_avg < 0: pred_avg += 100
            candidates[pred_avg] += 5

            # Recent 5 deltas
            recent_deltas = all_deltas[-5:]
            avg_recent = np.mean(recent_deltas)
            pred_recent = (yesterday_jodi + int(round(avg_recent))) % 100
            if pred_recent < 0: pred_recent += 100
            candidates[pred_recent] += 7

        total = sum(candidates.values()) or 1
        return [(v, w / total) for v, w in candidates.most_common(6)]


# ===========================================================
# AGENT 4: CycleAgent ? Modular Cycles + Gap Analysis
# ===========================================================
class CycleAgent:
    name = "CycleAgent"

    def predict(self, target_day_vals: List[int], **kwargs) -> List[Tuple[int, float]]:
        if len(target_day_vals) < 10:
            return []

        candidates = Counter()

        # Overdue numbers (longest gap since last seen)
        last_seen = {}
        for i, v in enumerate(target_day_vals):
            last_seen[v] = i
        current_idx = len(target_day_vals) - 1
        gaps = {v: current_idx - idx for v, idx in last_seen.items()}
        overdue = sorted(gaps.items(), key=lambda x: -x[1])[:10]
        for v, gap in overdue[:5]:
            candidates[v] += min(gap, 20)  # cap influence

        # Modular cycle detection (mod 3, 5, 7, 10)
        last_val = target_day_vals[-1]
        for mod in [3, 5, 7, 10]:
            remainder = last_val % mod
            # Find numbers with same remainder that appeared after current-similar values
            same_mod = [target_day_vals[i + 1] for i in range(len(target_day_vals) - 1)
                        if target_day_vals[i] % mod == remainder]
            if same_mod:
                c = Counter(same_mod)
                for v, cnt in c.most_common(3):
                    candidates[v] += cnt * 2

        # Self-follow patterns (what follows current last value)
        last_val = target_day_vals[-1]
        followers = [target_day_vals[i + 1] for i in range(len(target_day_vals) - 1)
                     if target_day_vals[i] == last_val]
        for v in followers:
            candidates[v] += 10

        # Tens-follow pattern
        last_tens = last_val // 10
        tens_followers = [target_day_vals[i + 1] for i in range(len(target_day_vals) - 1)
                          if target_day_vals[i] // 10 == last_tens]
        c_tf = Counter(tens_followers)
        for v, cnt in c_tf.most_common(5):
            candidates[v] += cnt

        # Units-follow pattern
        last_units = last_val % 10
        units_followers = [target_day_vals[i + 1] for i in range(len(target_day_vals) - 1)
                           if target_day_vals[i] % 10 == last_units]
        c_uf = Counter(units_followers)
        for v, cnt in c_uf.most_common(5):
            candidates[v] += cnt

        # Digit sum cycle
        last_dsum = (last_val // 10) + (last_val % 10)
        dsum_followers = [target_day_vals[i + 1] for i in range(len(target_day_vals) - 1)
                          if (target_day_vals[i] // 10 + target_day_vals[i] % 10) == last_dsum]
        c_dsf = Counter(dsum_followers)
        for v, cnt in c_dsf.most_common(3):
            candidates[v] += cnt * 2

        total = sum(candidates.values()) or 1
        return [(v, w / total) for v, w in candidates.most_common(8)]


class MirrorTraceAgent:
    name = "MirrorTraceAgent"

    def predict(self, target_day_vals: List[int], yesterday_jodi: int = None, **kwargs) -> List[Tuple[int, float]]:
        if not target_day_vals or yesterday_jodi is None:
            return []

        candidates = Counter()
        
        # Mirror map: 0->5, 1->6, 2->7, 3->8, 4->9
        MIRROR = {0:5, 1:6, 2:7, 3:8, 4:9, 5:0, 6:1, 7:2, 8:3, 9:4}
        
        y_tens = yesterday_jodi // 10
        y_units = yesterday_jodi % 10
        
        # 1. Full Mirror (74 -> 29)
        full_mirror = MIRROR[y_tens] * 10 + MIRROR[y_units]
        candidates[full_mirror] += 10
        
        # 2. Open Mirror (74 -> 24)
        open_mirror = MIRROR[y_tens] * 10 + y_units
        candidates[open_mirror] += 8
        
        # 3. Close Mirror (74 -> 79)
        close_mirror = y_tens * 10 + MIRROR[y_units]
        candidates[close_mirror] += 8
        
        # 4. Family Logic (4 numbers in a mirror set)
        family = [
            y_tens * 10 + y_units,
            MIRROR[y_tens] * 10 + y_units,
            y_tens * 10 + MIRROR[y_units],
            MIRROR[y_tens] * 10 + MIRROR[y_units]
        ]
        for f in family:
            if f != yesterday_jodi:
                candidates[f] += 5

        # 5. Historical Mirror Patterns
        # Look for times when target followed a mirror
        for i in range(len(target_day_vals) - 1):
            val = target_day_vals[i]
            target = target_day_vals[i+1]
            if val == full_mirror or val == open_mirror or val == close_mirror:
                candidates[target] += 3

        total = sum(candidates.values()) or 1
        return [(v, round(w / total, 3)) for v, w in candidates.most_common(6)]
class SeriesSpikeAgent:
    name = "SeriesSpikeAgent"

    def predict(self, target_day_vals: List[int], **kwargs) -> List[Tuple[int, float]]:
        if len(target_day_vals) < 15:
            return []
            
        candidates = Counter()
        recent_20 = target_day_vals[-20:]
        
        # Analyze tens-digit 'Heat'
        tens_heat = Counter(v // 10 for v in recent_20)
        top_tens = [t for t, _ in tens_heat.most_common(2)]
        
        # Analyze units-digit 'Heat'
        units_heat = Counter(v % 10 for v in recent_20)
        top_units = [u for u, _ in units_heat.most_common(2)]
        
        for t in top_tens:
            for u in top_units:
                # Numbers in the hot series get a boost
                candidates[t * 10 + u] += 10
                
        # Total-digit 'Heat' (Sum of digits)
        sum_heat = Counter(v // 10 + v % 10 for v in recent_20)
        top_sums = [s for s, _ in sum_heat.most_common(2)]
        
        for i in range(100):
            if (i // 10 + i % 10) in top_sums:
                candidates[i] += 5

        total = sum(candidates.values()) or 1
        return [(v, round(w / total, 3)) for v, w in candidates.most_common(6)]

class StepAgent:
    name = "StepAgent"

    def predict(self, target_day_vals: List[int], **kwargs) -> List[Tuple[int, float]]:
        if len(target_day_vals) < 10:
            return []
            
        candidates = Counter()
        diffs = [target_day_vals[i+1] - target_day_vals[i] for i in range(len(target_day_vals)-1)]
        
        # Look for repeated steps (deltas)
        recent_diffs = diffs[-15:]
        freq_diffs = Counter(recent_diffs)
        
        last_val = target_day_vals[-1]
        
        # Apply the most common steps to the last result
        for d, cnt in freq_diffs.most_common(3):
            pred = (last_val + d) % 100
            candidates[pred] += cnt * 5
            
        # Look for 'Lagged Steps' (Steps that repeat after X iterations)
        if len(diffs) > 10:
            for lag in range(2, 6):
                if diffs[-1] == diffs[-lag]:
                    # The pattern is repeating!
                    pred_lag = (last_val + diffs[-lag+1]) % 100
                    candidates[pred_lag] += 10

        total = sum(candidates.values()) or 1
        return [(v, round(w / total, 3)) for v, w in candidates.most_common(6)]


class MLAgent:
    name = "MLAgent"

    def predict(self, target_day_vals: List[int], **kwargs) -> List[Tuple[int, float]]:
        if len(target_day_vals) < WINDOW_SIZE + 10:
            return []

        check_ram("MLAgent start")

        X, yt, yu = build_enhanced_features(target_day_vals, WINDOW_SIZE)
        if len(X) == 0:
            return []

        # Try XGBoost GPU first, fall back to CPU
        try:
            import xgboost as xgb

            # Check if GPU is available
            try:
                gpu_params = {
                    'objective': 'multi:softprob',
                    'tree_method': 'hist',
                    'device': 'cuda',
                    'max_depth': 5,
                    'learning_rate': 0.05,
                    'n_estimators': 150,
                    'max_bin': 128,
                    'random_state': 42,
                    'verbosity': 0,
                    'n_jobs': 1,
                }
                # Tens model
                model_t = xgb.XGBClassifier(**gpu_params,
                                            num_class=10)
                model_t.fit(X, yt)

                # Units model
                model_u = xgb.XGBClassifier(**gpu_params,
                                            num_class=10)
                model_u.fit(X, yu)
                engine = "XGBoost-GPU (cuda)"

            except Exception:
                # Fallback to CPU
                cpu_params = {
                    'objective': 'multi:softprob',
                    'tree_method': 'hist',
                    'max_depth': 5,
                    'learning_rate': 0.05,
                    'n_estimators': 150,
                    'random_state': 42,
                    'verbosity': 0,
                    'n_jobs': -1,
                }
                model_t = xgb.XGBClassifier(**cpu_params,
                                            num_class=10)
                model_t.fit(X, yt)

                model_u = xgb.XGBClassifier(**cpu_params,
                                            num_class=10)
                model_u.fit(X, yu)
                engine = "XGBoost-CPU"

        except ImportError:
            # No XGBoost ? use sklearn fallback
            from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
            from sklearn.ensemble import VotingClassifier

            rf_t = RandomForestClassifier(n_estimators=150, max_depth=5,
                                          random_state=42, class_weight='balanced', n_jobs=-1)
            hgb_t = HistGradientBoostingClassifier(learning_rate=0.05, max_leaf_nodes=31, random_state=42)
            model_t = VotingClassifier(estimators=[('rf', rf_t), ('hgb', hgb_t)], voting='soft')
            model_t.fit(X, yt)

            rf_u = RandomForestClassifier(n_estimators=150, max_depth=5,
                                          random_state=42, class_weight='balanced', n_jobs=-1)
            hgb_u = HistGradientBoostingClassifier(learning_rate=0.05, max_leaf_nodes=31, random_state=42)
            model_u = VotingClassifier(estimators=[('rf', rf_u), ('hgb', hgb_u)], voting='soft')
            model_u.fit(X, yu)
            engine = "sklearn-RF+HGB"

        check_ram("MLAgent after training")

        # Predict using last window
        current_window = target_day_vals[-WINDOW_SIZE:]
        feat = _extract_window_features(current_window)
        X_pred = np.array([feat], dtype=np.float32)

        probs_t = model_t.predict_proba(X_pred)[0]
        probs_u = model_u.predict_proba(X_pred)[0]

        classes_t = model_t.classes_ if hasattr(model_t, 'classes_') else list(range(10))
        classes_u = model_u.classes_ if hasattr(model_u, 'classes_') else list(range(10))

        # Top jodi combinations
        jodi_probs = []
        for i, t in enumerate(classes_t):
            for j, u in enumerate(classes_u):
                prob = probs_t[i] * probs_u[j]
                jodi_probs.append((int(t) * 10 + int(u), prob))

        jodi_probs.sort(key=lambda x: x[1], reverse=True)
        print(f"    [{self.name}] Engine: {engine}")
        return jodi_probs[:8]


# ===========================================================
# AGENT 6: LLMAgent ? Ollama llama3.2:3b Reasoning
# ===========================================================
class LLMAgent:
    name = "LLMAgent"

    def predict(self, target_day_vals: List[int], yesterday_jodi: int = None,
                target_day: str = "TUE", yesterday_day: str = "MON",
                other_agent_results: Dict = None, **kwargs) -> List[Tuple[int, float]]:
        try:
            import requests
        except ImportError:
            print(f"    [{self.name}] requests library not available")
            return []

        # Build context for LLM
        recent_20 = target_day_vals[-20:] if len(target_day_vals) >= 20 else target_day_vals
        recent_str = ", ".join(f"{v:02d}" for v in recent_20)

        # Frequency analysis
        c20 = Counter(recent_20)
        freq_str = ", ".join(f"{v:02d}({cnt}x)" for v, cnt in c20.most_common(8))

        # Digit distribution
        tens_c = Counter(v // 10 for v in recent_20)
        units_c = Counter(v % 10 for v in recent_20)
        tens_str = ", ".join(f"{d}({c}x)" for d, c in tens_c.most_common(5))
        units_str = ", ".join(f"{d}({c}x)" for d, c in units_c.most_common(5))

        # Diffs
        diffs = [target_day_vals[i + 1] - target_day_vals[i]
                 for i in range(max(0, len(target_day_vals) - 11), len(target_day_vals) - 1)]
        diffs_str = ", ".join(f"{d:+d}" for d in diffs[-10:])

        # Other agents' predictions
        agents_str = ""
        if other_agent_results:
            for agent_name, preds in other_agent_results.items():
                if preds:
                    top3 = ", ".join(f"{v:02d}({p:.0%})" for v, p in preds[:3])
                    agents_str += f"  {agent_name}: {top3}\n"

        yesterday_str = f"\nYesterday ({yesterday_day}) Jodi was: {yesterday_jodi:02d}" if yesterday_jodi is not None else ""

        prompt = f"""You are a mathematical pattern analysis expert. Analyze these number sequences and predict the next number.

TASK: Predict today's ({target_day}) Jodi number (00-99).{yesterday_str}

DATA:
- Recent 20 {target_day} values: [{recent_str}]
- Frequency (recent 20): {freq_str}
- Tens digit distribution: {tens_str}
- Units digit distribution: {units_str}
- Recent diffs: [{diffs_str}]
- Last value: {target_day_vals[-1]:02d}

OTHER PREDICTION AGENTS' RESULTS:
{agents_str}
INSTRUCTIONS:
1. Look for repeating patterns, cycles, and mathematical relationships
2. Consider the tens and units digits separately
3. Factor in momentum/trend from recent differences
4. Consider what other agents predicted but form your own judgment
5. Respond with EXACTLY this format (nothing else):
PREDICTION: XX, YY, ZZ, WW
CONFIDENCE: high/medium/low
REASONING: one line explanation

Where XX is your #1 pick, YY is #2, ZZ is #3, WW is #4 (all two-digit 00-99)."""

        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": OLLAMA_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_ctx": 2048,
                        "temperature": 0.3,
                        "num_predict": 150,
                    }
                },
                timeout=OLLAMA_TIMEOUT
            )

            if response.status_code != 200:
                print(f"    [{self.name}] Ollama returned status {response.status_code}")
                return []

            result = response.json()
            text = result.get("response", "")
            return self._parse_response(text)

        except requests.exceptions.ConnectionError:
            print(f"    [{self.name}] Cannot connect to Ollama at {OLLAMA_URL}")
            return []
        except requests.exceptions.Timeout:
            print(f"    [{self.name}] Ollama timed out after {OLLAMA_TIMEOUT}s")
            return []
        except Exception as e:
            print(f"    [{self.name}] Error: {e}")
            return []

    def _parse_response(self, text: str) -> List[Tuple[int, float]]:
        """Parse LLM response to extract predictions."""
        results = []
        conf_map = {"high": 0.8, "medium": 0.5, "low": 0.3}

        # Extract confidence
        confidence = 0.5
        for line in text.split("\n"):
            line_upper = line.strip().upper()
            if "CONFIDENCE:" in line_upper:
                for level, val in conf_map.items():
                    if level.upper() in line_upper:
                        confidence = val
                        break

        # Extract predictions
        for line in text.split("\n"):
            if "PREDICTION:" in line.upper():
                # Extract numbers from the prediction line
                import re
                numbers = re.findall(r'\b(\d{1,2})\b', line)
                for i, num_str in enumerate(numbers[:4]):
                    num = int(num_str) % 100
                    # Decreasing confidence for lower-ranked picks
                    weight = confidence * (1.0 - i * 0.15)
                    results.append((num, weight))
                break

        if not results:
            # Try to find any two-digit numbers in the response
            import re
            numbers = re.findall(r'\b(\d{2})\b', text)
            for i, num_str in enumerate(numbers[:4]):
                num = int(num_str) % 100
                results.append((num, 0.3 * (1.0 - i * 0.15)))

        # Print LLM reasoning
        for line in text.split("\n"):
            if "REASONING:" in line.upper():
                print(f"    [LLMAgent] {line.strip()}")
                break

        return results


# ===========================================================
# SWARM ENSEMBLE ? Weighted Vote
# ===========================================================
def ensemble_vote(agent_results: Dict[str, List[Tuple[int, float]]]) -> List[Tuple[int, float]]:
    """Weighted ensemble vote across all agents."""
    scores = Counter()
    for agent_name, preds in agent_results.items():
        weight = AGENT_WEIGHTS.get(agent_name, 0.10)
        for jodi, prob in preds:
            scores[jodi] += prob * weight

    total = sum(scores.values()) or 1
    final = [(v, round(w / total, 4)) for v, w in scores.most_common(10)]
    return final


# ===========================================================
# MAIN SWARM PREDICTOR
# ===========================================================
def run_swarm(target_day: str = "TUE", yesterday_day: str = "MON",
              yesterday_jodi: int = 74) -> List[Tuple[int, float]]:
    """Run all 6 agents and return ensemble predictions."""

    print()
    print("=" * 70)
    print("  SWARM PREDICTOR v1.0 ? MiroFish-Inspired Multi-Agent Engine")
    print(f"  Predicting: {target_day} | Yesterday ({yesterday_day}) = {yesterday_jodi:02d}")
    print(f"  RAM Limit: {RAM_LIMIT_GB} GB | Ollama: {OLLAMA_URL} ({OLLAMA_MODEL})")
    print("=" * 70)
    print()

    check_ram("Initial")

    # Load data
    data = load_all_data()
    target_vals = data.get(target_day, [])
    yesterday_vals = data.get(yesterday_day, [])

    print(f"  {target_day} history: {len(target_vals)} values | Last 5: {', '.join(f'{v:02d}' for v in target_vals[-5:])}")
    print(f"  {yesterday_day} history: {len(yesterday_vals)} values | Last 5: {', '.join(f'{v:02d}' for v in yesterday_vals[-5:])}")
    print()

    agent_results = {}
    agents = [
        ("StatAgent", StatAgent()),
        ("TrendAgent", TrendAgent()),
        ("TransitionAgent", TransitionAgent()),
        ("CycleAgent", CycleAgent()),
        ("MirrorTraceAgent", MirrorTraceAgent()),
        ("SeriesSpikeAgent", SeriesSpikeAgent()), # INTEGRATED
        ("StepAgent", StepAgent()),               # INTEGRATED
        ("HistoryAgent", HistoryAgent()),         # NEW: 14-Year Trick Analysis
        ("MLAgent", MLAgent()),
    ]

    # Run agents 1-5 first (so LLM can see their results)
    for agent_name, agent in agents:
        print("-" * 60)
        print(f"  AGENT: {agent_name} (weight: {AGENT_WEIGHTS.get(agent_name, 0):.0%})")
        print("-" * 60)
        t0 = time.time()

        try:
            preds = agent.predict(
                target_day_vals=target_vals,
                yesterday_vals=yesterday_vals,
                yesterday_jodi=yesterday_jodi,
                target_day=target_day,
                yesterday_day=yesterday_day,
            )
        except Exception as e:
            print(f"    ERROR: {e}")
            preds = []

        elapsed = time.time() - t0
        agent_results[agent_name] = preds

        if preds:
            for i, (jodi, prob) in enumerate(preds[:4]):
                marker = ">>>" if i == 0 else "   "
                print(f"    {marker} #{i + 1}: {jodi:02d}  ({prob:.1%})")
        else:
            print(f"    No predictions generated")
        print(f"    [{elapsed:.1f}s | RAM: {check_ram():.2f} GB]")
        print()

    # Run LLMAgent last (with other agents' results as context)
    print(f"  {'-' * 60}")
    print(f"  AGENT: LLMAgent (weight: {AGENT_WEIGHTS.get('LLMAgent', 0):.0%})")
    print(f"  {'-' * 60}")
    t0 = time.time()
    llm_agent = LLMAgent()
    try:
        llm_preds = llm_agent.predict(
            target_day_vals=target_vals,
            yesterday_jodi=yesterday_jodi,
            target_day=target_day,
            yesterday_day=yesterday_day,
            other_agent_results=agent_results,
        )
    except Exception as e:
        print(f"    ERROR: {e}")
        llm_preds = []

    elapsed = time.time() - t0
    agent_results["LLMAgent"] = llm_preds
    if llm_preds:
        for i, (jodi, prob) in enumerate(llm_preds[:4]):
            marker = ">>>" if i == 0 else "   "
            print(f"    {marker} #{i + 1}: {jodi:02d}  ({prob:.1%})")
    else:
        print(f"    No predictions from LLM")
    print(f"    [{elapsed:.1f}s | RAM: {check_ram():.2f} GB]")
    print()

    # Final ensemble
    final = ensemble_vote(agent_results)

    # Mirror-Symmetry Correction (Ensuring no 1-6 or 2-7 Cut Errors)
    mirror_final = []
    seen = set()
    for jodi, weight in final:
        if jodi in seen: continue
        mirror_final.append((jodi, weight))
        seen.add(jodi)
        
        # Calculate full cut
        t, u = jodi // 10, jodi % 10
        fc = MIRROR[t] * 10 + MIRROR[u]
        if fc not in seen:
            # Promote full cut with 90% of the original's confidence
            mirror_final.append((fc, weight * 0.9))
            seen.add(fc)
            
    mirror_final.sort(key=lambda x: x[1], reverse=True)
    final = mirror_final[:10]

    print("=" * 70)
    print("  *** SWARM ENSEMBLE PREDICTION (PHASE-AWARE) ***")
    print("=" * 70)
    print()
    for i, (jodi, weight) in enumerate(final[:6]):
        rank = ["1st", "2nd", "3rd", "4th", "5th", "6th"][i]
        marker = "  >>>  " if i == 0 else "       "
        print(f"  {marker}{rank} Choice:  {jodi:02d}   (confidence: {weight:.1%})")
    print()
    print(f"  Yesterday {yesterday_day} = {yesterday_jodi:02d}")
    print(f"  Today {target_day} Prediction = {final[0][0]:02d} (primary)")
    print(f"  Mirror Successor = {final[1][0]:02d} (backup)")
    print()


    # Agent agreement analysis
    agent_top1 = {}
    for name, preds in agent_results.items():
        if preds:
            agent_top1[name] = preds[0][0]
    print("  Agent Agreement:")
    top1_counter = Counter(agent_top1.values())
    for jodi, cnt in top1_counter.most_common(5):
        agreeing = [n for n, v in agent_top1.items() if v == jodi]
        print(f"    {jodi:02d}: {cnt} agents agree ? {', '.join(agreeing)}")
    print()
    print(f"  Total RAM used: {check_ram('Final'):.2f} GB")
    print("=" * 70)
    print()

    return final


# ===========================================================
# CLI ENTRY POINT
# ===========================================================
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Swarm Predictor - MiroFish Inspired")
    # Try to load latest_state.json for defaults
    def_day, def_y_day, def_y_jodi = "MON", "SAT", 00
    if os.path.exists("latest_state.json"):
        try:
            with open("latest_state.json", "r") as f:
                state = json.load(f)
                def_y_jodi = state.get("latest_result", 0)
                def_y_day = state.get("day", "MON")
                # Target day is usually next in sequence
                idx = DAYS.index(def_y_day)
                def_day = DAYS[(idx + 1) % len(DAYS)]
        except: pass

    parser.add_argument("--day", default=def_day, help="Day to predict")
    parser.add_argument("--yesterday-day", default=def_y_day, help="Yesterday's day")
    parser.add_argument("--yesterday-jodi", type=int, default=def_y_jodi, help="Yesterday's Jodi")
    args = parser.parse_args()

    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")
    run_swarm(
        target_day=args.day.upper(),
        yesterday_day=args.yesterday_day.upper(),
        yesterday_jodi=args.yesterday_jodi,
    )
