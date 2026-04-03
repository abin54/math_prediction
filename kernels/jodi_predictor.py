"""
Jodi Number Predictor (Integrated with LightFish)
===================================================
Combines LLM-based prediction (via Ollama on NVIDIA GPU) with LightFish-style
statistical pattern detection for ensemble Jodi number forecasting.

Hardware-aware:
  * Forces NVIDIA GPU (not integrated graphics)
  * Caps VRAM usage to protect a 4GB GTX 1650
  * Limits RAM footprint for 8GB systems
  * Sequential LLM calls (1 at a time) to avoid OOM

Statistical methods (zero GPU cost):
  * Arithmetic / geometric / quadratic progression detection
  * Fibonacci-like sequence detection
  * Weighted moving average with trend
  * Frequency-based mode prediction
  * Modular digit-sum analysis (exploits the Jodi formula)
"""

from __future__ import annotations

import io
import logging
import math
import os
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

# ──────────────────────────────────────────────
# FORCE NVIDIA GPU & LIMIT RESOURCES
# Must be set BEFORE importing ollama / torch
# ──────────────────────────────────────────────
os.environ["CUDA_VISIBLE_DEVICES"] = "0"           # Force first NVIDIA GPU only
os.environ["OLLAMA_NUM_PARALLEL"] = "1"             # One request at a time
os.environ["OLLAMA_MAX_LOADED_MODELS"] = "1"        # Only one model in VRAM
os.environ["OLLAMA_GPU_MEMORY"] = "3072"            # Cap at 3GB of 4GB VRAM
os.environ["CUDA_LAUNCH_BLOCKING"] = "1"            # Synchronous GPU ops (safer)

import pandas as pd

try:
    import ollama
except ImportError:
    print("ERROR: 'ollama' package not found. Install with:  pip install ollama")
    sys.exit(1)

# --- Ensure UTF-8 output on Windows consoles ---
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ──────────────────────────────────────────────
# LOGGING
# ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────
@dataclass(frozen=True)
class Config:
    excel_file: str = "Number_Chart.xlsx"
    sheet_name: str = "Numeric Analysis"
    model_name: str = "llama3.2:3b"
    history_len: int = 10
    days: tuple[str, ...] = ("MON", "TUE", "WED", "THU", "FRI", "SAT")
    max_retries: int = 3
    retry_delay: float = 1.0
    export_results: bool = True
    # --- GPU / RAM limits (for Ollama generate options) ---
    num_gpu_layers: int = 20          # Offload 20 layers to GPU (rest on CPU)
    num_ctx: int = 512                # Small context window = less VRAM
    num_thread: int = 4               # CPU threads for non-GPU layers
    temperature: float = 0.3          # Low temp = more deterministic


CFG = Config()


# ──────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────
def load_jodi_series(cfg: Config = CFG) -> dict[str, list[int]]:
    """Read the 'Numeric Analysis' sheet and return ``{day: [values]}``."""
    path = Path(cfg.excel_file)
    if not path.exists():
        log.error("Excel file not found: %s", path.resolve())
        sys.exit(1)

    df = pd.read_excel(path, sheet_name=cfg.sheet_name, header=0)

    series: dict[str, list[int]] = {}
    for day in cfg.days:
        col = f"{day} Jodi Num"
        if col not in df.columns:
            raise KeyError(f"Column '{col}' missing from sheet '{cfg.sheet_name}'.")
        vals = pd.to_numeric(df[col], errors="coerce").dropna().astype(int).tolist()
        series[day] = vals
        log.info("%-3s : %d valid entries loaded", day, len(vals))

    return series


# ══════════════════════════════════════════════
# LIGHTFISH STATISTICAL PREDICTOR (integrated)
# ══════════════════════════════════════════════

class StatisticalPredictor:
    """LightFish-style statistical pattern detector for number sequences."""

    @staticmethod
    def detect_pattern(seq: list[float]) -> dict:
        """Detect mathematical patterns in a sequence."""
        if len(seq) < 2:
            return {"type": "insufficient"}

        diffs = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]

        # Arithmetic progression
        if len(set(diffs)) == 1:
            return {"type": "arithmetic", "diff": diffs[0]}

        # Geometric progression
        ratios = []
        for i in range(len(seq) - 1):
            if seq[i] != 0:
                ratios.append(seq[i + 1] / seq[i])
            else:
                ratios.append(float("inf"))
        if len(set(ratios)) == 1 and ratios[0] != float("inf"):
            return {"type": "geometric", "ratio": ratios[0]}

        # Quadratic (second-differences constant)
        if len(diffs) >= 2:
            second_diffs = [diffs[i + 1] - diffs[i] for i in range(len(diffs) - 1)]
            if len(set(second_diffs)) == 1:
                return {"type": "quadratic", "second_diff": second_diffs[0]}

        # Alternating pattern
        if len(seq) >= 4:
            even_pos = [seq[i] for i in range(0, len(seq), 2)]
            odd_pos = [seq[i] for i in range(1, len(seq), 2)]
            if len(set(even_pos)) == 1 and len(set(odd_pos)) == 1:
                return {"type": "alternating", "even_val": even_pos[0], "odd_val": odd_pos[0]}

        # Fibonacci-like
        if len(seq) >= 3:
            fib = all(abs(seq[i] - (seq[i - 1] + seq[i - 2])) < 1e-6 for i in range(2, len(seq)))
            if fib:
                return {"type": "fibonacci"}

        return {"type": "unknown"}

    @staticmethod
    def predict_from_pattern(seq: list[float]) -> dict:
        """Predict next value based on detected pattern."""
        if not seq:
            return {"prediction": None, "confidence": 0.0, "method": "empty"}
        if len(seq) == 1:
            return {"prediction": seq[0], "confidence": 0.3, "method": "single_value"}

        pattern = StatisticalPredictor.detect_pattern(seq)

        if pattern["type"] == "arithmetic":
            return {
                "prediction": seq[-1] + pattern["diff"],
                "confidence": 0.95,
                "method": "arithmetic_progression",
            }
        elif pattern["type"] == "geometric":
            return {
                "prediction": seq[-1] * pattern["ratio"],
                "confidence": 0.9,
                "method": "geometric_progression",
            }
        elif pattern["type"] == "quadratic":
            diffs = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
            next_diff = diffs[-1] + pattern["second_diff"]
            return {
                "prediction": round(seq[-1] + next_diff, 4),
                "confidence": 0.7,
                "method": "quadratic_extrapolation",
            }
        elif pattern["type"] == "alternating":
            val = pattern["odd_val"] if len(seq) % 2 == 0 else pattern["even_val"]
            return {"prediction": val, "confidence": 0.85, "method": "alternating_pattern"}
        elif pattern["type"] == "fibonacci":
            return {
                "prediction": seq[-1] + seq[-2],
                "confidence": 0.8,
                "method": "fibonacci_like",
            }
        else:
            return StatisticalPredictor._weighted_trend(seq)

    @staticmethod
    def _weighted_trend(seq: list[float]) -> dict:
        """Weighted moving average with trend — fallback method."""
        n = min(len(seq), 5)
        weights = list(range(1, n + 1))
        recent = seq[-n:]
        wma = sum(v * w for v, w in zip(recent, weights)) / sum(weights)
        trend = (seq[-1] - seq[-n]) / n if n > 1 else 0
        pred = wma + trend
        return {
            "prediction": round(pred, 2),
            "confidence": 0.35,
            "method": "weighted_moving_avg",
        }

    @staticmethod
    def frequency_prediction(seq: list[int], top_n: int = 3) -> dict:
        """Predict based on most frequent values in the sequence."""
        c = Counter(seq)
        most_common = c.most_common(top_n)
        return {
            "prediction": most_common[0][0],
            "confidence": most_common[0][1] / len(seq),
            "method": "frequency_mode",
            "top_candidates": [(v, cnt) for v, cnt in most_common],
        }

    @staticmethod
    def modular_prediction(seq: list[int]) -> dict:
        """
        Predict using digit-sum modular analysis.
        Since Jodi = (digit_sum_of_Open mod 10)(digit_sum_of_Close mod 10),
        we analyse the tens and units digits independently.
        """
        if len(seq) < 3:
            return {"prediction": None, "confidence": 0.0, "method": "modular_insufficient"}

        tens = [v // 10 for v in seq]
        units = [v % 10 for v in seq]

        # Most common recent tens and units digits (last 20)
        recent_tens = tens[-20:]
        recent_units = units[-20:]

        tc = Counter(recent_tens).most_common(3)
        uc = Counter(recent_units).most_common(3)

        pred_tens = tc[0][0]
        pred_units = uc[0][0]

        return {
            "prediction": pred_tens * 10 + pred_units,
            "confidence": 0.25,
            "method": "modular_digit_analysis",
            "tens_candidates": tc,
            "units_candidates": uc,
        }


# ══════════════════════════════════════════════
# LLM PREDICTION (resource-limited Ollama)
# ══════════════════════════════════════════════

_NUMBER_RE = re.compile(r"-?\d+\.?\d*")


def _build_prompt(day: str, history: list[int]) -> str:
    seq = ", ".join(map(str, history))
    return (
        "You are a pure mathematics sequence analyst. "
        "This is a university-level number theory exercise.\n\n"
        f"A professor has given you the last {len(history)} values "
        f"from a deterministic integer sequence labelled '{day}':\n"
        f"{seq}\n\n"
        "Each value is between 0 and 99 inclusive.\n"
        "Analyse the differences, modular arithmetic patterns, "
        "periodicity, and any recurring cycles.\n\n"
        "Based on your mathematical analysis, what is the single "
        "most likely next integer in this sequence?\n\n"
        "Respond with ONLY one integer (0-99). No words, no explanation."
    )


def predict_next_llm(
    day: str,
    history: list[int],
    cfg: Config = CFG,
) -> Optional[int]:
    """Call Ollama with resource-limited options; retry with back-off."""
    prompt = _build_prompt(day, history)
    delay = cfg.retry_delay

    for attempt in range(1, cfg.max_retries + 1):
        try:
            resp = ollama.chat(
                model=cfg.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={
                    "num_gpu": cfg.num_gpu_layers,
                    "num_ctx": cfg.num_ctx,
                    "num_thread": cfg.num_thread,
                    "temperature": cfg.temperature,
                    "num_predict": 16,        # We only need a short answer
                    "low_vram": True,          # Ollama low-VRAM mode
                },
            )
            answer: str = resp["message"]["content"].strip()
            match = _NUMBER_RE.search(answer)
            if match:
                val = int(float(match.group()))
                if 0 <= val <= 99:
                    return val
                log.warning("%s attempt %d -- out of range: %d", day, attempt, val)
            else:
                log.warning("%s attempt %d -- non-numeric: %s", day, attempt, answer[:80])
        except Exception as exc:
            log.warning("%s attempt %d -- error: %s", day, attempt, exc)

        if attempt < cfg.max_retries:
            time.sleep(delay)
            delay *= 2

    return None


# ══════════════════════════════════════════════
# ENSEMBLE PREDICTOR
# ══════════════════════════════════════════════

def ensemble_predict(
    day: str,
    full_history: list[int],
    cfg: Config = CFG,
) -> dict:
    """
    Combine LLM + multiple statistical methods, then pick the best
    or average the results weighted by confidence.
    """
    recent = full_history[-cfg.history_len:]
    results = []

    # --- Method 1: Pattern detection (LightFish) ---
    pat = StatisticalPredictor.predict_from_pattern([float(x) for x in recent])
    if pat["prediction"] is not None:
        pred = int(round(pat["prediction"])) % 100
        results.append((pred, pat["confidence"], pat["method"]))
        log.info("  %s [%s] -> %d (conf %.2f)", day, pat["method"], pred, pat["confidence"])

    # --- Method 2: Frequency-based ---
    freq = StatisticalPredictor.frequency_prediction(full_history)
    results.append((freq["prediction"], freq["confidence"], freq["method"]))
    log.info("  %s [%s] -> %d (conf %.2f)", day, freq["method"], freq["prediction"], freq["confidence"])

    # --- Method 3: Modular digit analysis ---
    mod = StatisticalPredictor.modular_prediction(full_history)
    if mod["prediction"] is not None:
        results.append((mod["prediction"], mod["confidence"], mod["method"]))
        log.info("  %s [%s] -> %d (conf %.2f)", day, mod["method"], mod["prediction"], mod["confidence"])

    # --- Method 4: LLM (heaviest — run last, sequentially) ---
    log.info("  %s [LLM %s] calling...", day, cfg.model_name)
    llm_pred = predict_next_llm(day, recent, cfg)
    if llm_pred is not None:
        results.append((llm_pred, 0.50, f"LLM ({cfg.model_name})"))
        log.info("  %s [LLM] -> %d (conf 0.50)", day, llm_pred)
    else:
        log.warning("  %s [LLM] failed, skipping", day)

    # --- Ensemble: weighted vote ---
    if not results:
        return {"day": day, "prediction": None, "method": "none", "details": []}

    # Weighted vote: each method votes for its prediction, weight = confidence
    vote_weights: dict[int, float] = {}
    for pred, conf, _ in results:
        vote_weights[pred] = vote_weights.get(pred, 0.0) + conf

    best_pred = max(vote_weights, key=vote_weights.get)  # type: ignore
    best_weight = vote_weights[best_pred]
    total_weight = sum(vote_weights.values())

    return {
        "day": day,
        "prediction": best_pred,
        "ensemble_confidence": round(best_weight / total_weight, 3),
        "method": "ensemble_weighted_vote",
        "details": [(p, c, m) for p, c, m in results],
    }


# ══════════════════════════════════════════════
# EXPORT RESULTS
# ══════════════════════════════════════════════

def export_predictions(
    predictions: dict[str, dict],
    cfg: Config = CFG,
) -> None:
    """Append a 'Predictions' sheet to the workbook."""
    rows = []
    for day, info in predictions.items():
        pred = info.get("prediction")
        conf = info.get("ensemble_confidence", 0)
        method = info.get("method", "")
        details = info.get("details", [])
        detail_str = " | ".join(f"{m}={p}" for p, c, m in details) if details else ""
        rows.append({
            "Day": day,
            "Predicted Jodi": pred if pred is not None else "N/A",
            "Confidence": f"{conf:.1%}",
            "Method": method,
            "Breakdown": detail_str,
        })
    df = pd.DataFrame(rows)

    with pd.ExcelWriter(
        cfg.excel_file, engine="openpyxl", mode="a", if_sheet_exists="replace"
    ) as writer:
        df.to_excel(writer, sheet_name="Predictions", index=False)

    log.info("Predictions written to 'Predictions' sheet in %s", cfg.excel_file)


# ══════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════

def print_gpu_info():
    """Show GPU status at startup."""
    try:
        import subprocess
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.used,memory.free,temperature.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode == 0:
            parts = [p.strip() for p in r.stdout.strip().split(",")]
            log.info("GPU: %s | VRAM: %s/%s MB (free %s MB) | Temp: %s C",
                     parts[0], parts[2], parts[1], parts[3], parts[4])
    except Exception:
        log.warning("Could not query NVIDIA GPU (nvidia-smi not found)")


def main() -> None:
    print_gpu_info()

    log.info("CUDA_VISIBLE_DEVICES=%s", os.environ.get("CUDA_VISIBLE_DEVICES", "not set"))
    log.info("Resource limits: GPU layers=%d, ctx=%d, threads=%d, low_vram=True",
             CFG.num_gpu_layers, CFG.num_ctx, CFG.num_thread)
    log.info("Loading Jodi series from '%s'...", CFG.excel_file)

    jodi_data = load_jodi_series()

    log.info("Running ensemble predictions (LightFish stats + LLM)...")
    predictions: dict[str, dict] = {}

    # SEQUENTIAL — one day at a time to protect GPU memory
    for day in CFG.days:
        hist = jodi_data[day]
        if len(hist) < 2:
            log.warning("%s -- not enough data (need >= 2, got %d)", day, len(hist))
            predictions[day] = {"day": day, "prediction": None, "method": "insufficient_data", "details": []}
            continue

        result = ensemble_predict(day, hist)
        predictions[day] = result

    # ── Pretty-print results ──
    print("\n+===================================+")
    print("|       JODI PREDICTIONS (Ensemble) |")
    print("+===================================+")
    for day in CFG.days:
        info = predictions.get(day, {})
        pred = info.get("prediction")
        conf = info.get("ensemble_confidence", 0)
        display = f"{pred:02d}" if pred is not None else "N/A"
        print(f"|  {day:<4}  ->  {display:>4}   (conf {conf:.0%})     |")
    print("+===================================+")

    # Show breakdown
    print("\n--- Method Breakdown ---")
    for day in CFG.days:
        info = predictions.get(day, {})
        details = info.get("details", [])
        if details:
            parts = [f"{m}={p:02d}" for p, c, m in details]
            print(f"  {day}: {' | '.join(parts)}")

    if CFG.export_results:
        try:
            export_predictions(predictions)
        except Exception as exc:
            log.warning("Could not write predictions to Excel: %s", exc)

    print()


if __name__ == "__main__":
    main()
