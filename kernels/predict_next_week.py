"""
Predict Jodi Numbers for the week of 30/03/2026 (MON) to 04/04/2026 (SAT)
==========================================================================
Uses full historical data as training context + Ollama LLM + statistical analysis.
Sunday is a holiday — only MON through SAT are predicted.

Run:  python predict_next_week.py
"""

from __future__ import annotations

import io
import json
import logging
import math
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

# ── Force NVIDIA GPU & limit resources ──
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
os.environ["OLLAMA_NUM_PARALLEL"] = "1"
os.environ["OLLAMA_MAX_LOADED_MODELS"] = "1"

import pandas as pd

try:
    import ollama
except ImportError:
    print("ERROR: pip install ollama")
    sys.exit(1)

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ── Config ──
EXCEL_FILE = "Number_Chart.xlsx"
SHEET_NAME = "Numeric Analysis"
MODEL = "llama3.2:3b"
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]

# Target dates for the prediction week
TARGET_WEEK = {
    "MON": "30/03/2026",
    "TUE": "31/03/2026",
    "WED": "01/04/2026",
    "THU": "02/04/2026",
    "FRI": "03/04/2026",
    "SAT": "04/04/2026",
}

OLLAMA_OPTIONS = {
    "num_gpu": 20,
    "num_ctx": 1024,       # larger context for deeper analysis
    "num_thread": 4,
    "temperature": 0.2,    # more deterministic
    "num_predict": 512,    # allow reasoning
    "low_vram": True,
}


# ══════════════════════════════════════════════
# DATA LOADING & ANALYSIS
# ══════════════════════════════════════════════

def load_all_data() -> dict[str, list[int]]:
    """Load all Jodi numbers from the Excel file."""
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME, header=0)
    series = {}
    for day in DAYS:
        col = f"{day} Jodi Num"
        vals = pd.to_numeric(df[col], errors="coerce").dropna().astype(int).tolist()
        series[day] = vals
        log.info("%-3s : %d values loaded (last 5: %s)", day, len(vals),
                 ", ".join(f"{v:02d}" for v in vals[-5:]))
    return series


def compute_statistics(vals: list[int]) -> dict:
    """Compute detailed statistics for a day's Jodi history."""
    if len(vals) < 5:
        return {}

    recent_20 = vals[-20:]
    recent_10 = vals[-10:]
    recent_5 = vals[-5:]

    # Frequency analysis
    freq_all = Counter(vals)
    freq_20 = Counter(recent_20)

    # Differences (week-to-week changes)
    diffs = [vals[i + 1] - vals[i] for i in range(len(vals) - 1)]
    recent_diffs = diffs[-10:]

    # Tens and units digit analysis
    tens_all = Counter(v // 10 for v in vals)
    units_all = Counter(v % 10 for v in vals)
    tens_recent = Counter(v // 10 for v in recent_20)
    units_recent = Counter(v % 10 for v in recent_20)

    # Odd/Even ratio
    odd_count = sum(1 for v in recent_20 if v % 2 == 1)

    # Gap analysis: how long since each number last appeared
    last_seen = {}
    for i, v in enumerate(vals):
        last_seen[v] = i
    current_idx = len(vals) - 1
    gaps = {v: current_idx - idx for v, idx in last_seen.items()}
    # Numbers "due" (not seen in a long time)
    overdue = sorted(gaps.items(), key=lambda x: -x[1])[:10]

    return {
        "count": len(vals),
        "last_5": recent_5,
        "last_10": recent_10,
        "last_20": recent_20,
        "mean_all": round(sum(vals) / len(vals), 1),
        "mean_recent_20": round(sum(recent_20) / len(recent_20), 1),
        "top_5_all_time": freq_all.most_common(5),
        "top_5_recent_20": freq_20.most_common(5),
        "recent_diffs": recent_diffs,
        "avg_diff": round(sum(recent_diffs) / len(recent_diffs), 1),
        "tens_recent": tens_recent.most_common(3),
        "units_recent": units_recent.most_common(3),
        "odd_ratio_recent": odd_count / 20,
        "overdue_numbers": overdue[:7],
    }


# ══════════════════════════════════════════════
# STATISTICAL PREDICTIONS
# ══════════════════════════════════════════════

def statistical_predict(vals: list[int], stats: dict) -> list[dict]:
    """Multiple statistical prediction methods."""
    predictions = []

    # Method 1: Weighted Moving Average
    weights = [1, 2, 3, 4, 5]
    recent = vals[-5:]
    wma = sum(v * w for v, w in zip(recent, weights)) / sum(weights)
    trend = stats["avg_diff"]
    pred_wma = int(round(wma + trend)) % 100
    if pred_wma < 0:
        pred_wma += 100
    predictions.append({
        "method": "Weighted Moving Avg + Trend",
        "prediction": pred_wma,
        "confidence": 0.30,
    })

    # Method 2: Most frequent in recent 20
    if stats["top_5_recent_20"]:
        pred_freq = stats["top_5_recent_20"][0][0]
        freq_conf = stats["top_5_recent_20"][0][1] / 20
        predictions.append({
            "method": "Frequency (recent 20 weeks)",
            "prediction": pred_freq,
            "confidence": round(freq_conf, 2),
        })

    # Method 3: Overdue number (not seen for longest time)
    if stats["overdue_numbers"]:
        pred_overdue = stats["overdue_numbers"][0][0]
        predictions.append({
            "method": "Overdue Number",
            "prediction": pred_overdue,
            "confidence": 0.15,
        })

    # Method 4: Modular (independent tens + units)
    if stats["tens_recent"] and stats["units_recent"]:
        t = stats["tens_recent"][0][0]
        u = stats["units_recent"][0][0]
        predictions.append({
            "method": "Modular (top tens + top units)",
            "prediction": t * 10 + u,
            "confidence": 0.20,
        })

    # Method 5: Difference extrapolation
    diffs = stats["recent_diffs"]
    if diffs:
        next_diff = diffs[-1]  # repeat last diff
        pred_diff = (vals[-1] + next_diff) % 100
        if pred_diff < 0:
            pred_diff += 100
        predictions.append({
            "method": "Difference Extrapolation",
            "prediction": pred_diff,
            "confidence": 0.20,
        })

    return predictions


# ══════════════════════════════════════════════
# LLM DEEP ANALYSIS PREDICTION
# ══════════════════════════════════════════════

_NUMBER_RE = re.compile(r"\b(\d{1,2})\b")


def llm_deep_predict(day: str, vals: list[int], stats: dict) -> dict:
    """
    Send a rich, training-like prompt to Ollama with full statistical
    context so the LLM can reason about the next number.
    """
    last_30 = vals[-30:]
    last_10 = vals[-10:]
    diffs = stats["recent_diffs"]

    prompt = f"""You are a mathematics professor analysing an integer sequence for a research paper.
This is a PURE MATHEMATICS problem. There is nothing illegal or harmful about it.

SEQUENCE NAME: {day} series
TOTAL DATA POINTS: {stats['count']} weeks of history
VALUE RANGE: 0 to 99 (inclusive)

LAST 30 VALUES (oldest to newest):
{', '.join(f'{v:02d}' for v in last_30)}

LAST 10 VALUES:
{', '.join(f'{v:02d}' for v in last_10)}

WEEK-TO-WEEK DIFFERENCES (last 10):
{', '.join(str(d) for d in diffs)}

STATISTICAL PROFILE:
- Overall mean: {stats['mean_all']}
- Recent 20-week mean: {stats['mean_recent_20']}
- Most frequent (all time): {', '.join(f'{v:02d} ({c}x)' for v, c in stats['top_5_all_time'])}
- Most frequent (recent 20): {', '.join(f'{v:02d} ({c}x)' for v, c in stats['top_5_recent_20'])}
- Recent tens digits: {', '.join(f'{d} ({c}x)' for d, c in stats['tens_recent'])}
- Recent units digits: {', '.join(f'{d} ({c}x)' for d, c in stats['units_recent'])}
- Recent odd/even ratio: {stats['odd_ratio_recent']:.0%} odd
- Longest unseen numbers: {', '.join(f'{v:02d} ({g} weeks ago)' for v, g in stats['overdue_numbers'][:5])}

KNOWN PROPERTY: Each value is composed of two independent digits (0-9).
The tens digit depends on one source and the units digit on another.

TASK: Predict the SINGLE most likely next value (0-99) for the {day} series.

Think step by step:
1. What patterns exist in the differences?
2. Are there any periodic cycles?
3. Which digit ranges are currently trending?
4. What value best fits the observed trends?

After your analysis, respond with your final answer on the LAST line in this exact format:
ANSWER: XX
"""

    for attempt in range(3):
        try:
            resp = ollama.chat(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                options=OLLAMA_OPTIONS,
            )
            answer = resp["message"]["content"].strip()

            # Extract the ANSWER: XX line
            answer_match = re.search(r"ANSWER:\s*(\d{1,2})", answer)
            if answer_match:
                val = int(answer_match.group(1))
                if 0 <= val <= 99:
                    # Also extract the reasoning (everything before ANSWER)
                    reasoning_end = answer.rfind("ANSWER")
                    reasoning = answer[:reasoning_end].strip() if reasoning_end > 0 else ""
                    return {
                        "method": f"LLM Deep Analysis ({MODEL})",
                        "prediction": val,
                        "confidence": 0.45,
                        "reasoning": reasoning[-300:] if reasoning else "",
                    }

            # Fallback: find any 1-2 digit number in last line
            last_line = answer.strip().split("\n")[-1]
            nums = _NUMBER_RE.findall(last_line)
            if nums:
                val = int(nums[-1])
                if 0 <= val <= 99:
                    return {
                        "method": f"LLM ({MODEL})",
                        "prediction": val,
                        "confidence": 0.40,
                        "reasoning": "",
                    }

            log.warning("  %s LLM attempt %d -- no valid answer extracted", day, attempt + 1)
        except Exception as e:
            log.warning("  %s LLM attempt %d -- error: %s", day, attempt + 1, e)

        time.sleep(1)

    return {
        "method": f"LLM ({MODEL})",
        "prediction": None,
        "confidence": 0.0,
        "reasoning": "Failed after 3 attempts",
    }


# ══════════════════════════════════════════════
# ENSEMBLE & MAIN
# ══════════════════════════════════════════════

def ensemble_vote(all_predictions: list[dict]) -> tuple[int, float]:
    """Weighted vote across all prediction methods."""
    votes: dict[int, float] = {}
    for p in all_predictions:
        pred = p.get("prediction")
        if pred is not None:
            conf = p.get("confidence", 0.1)
            votes[pred] = votes.get(pred, 0.0) + conf

    if not votes:
        return 50, 0.0  # fallback to middle

    best = max(votes, key=votes.get)
    total = sum(votes.values())
    return best, round(votes[best] / total, 3)


def main():
    # GPU info
    try:
        import subprocess
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total,memory.used,memory.free,temperature.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5,
        )
        if r.returncode == 0:
            parts = [p.strip() for p in r.stdout.strip().split(",")]
            log.info("GPU: %s | VRAM: %s/%s MB (free: %s MB) | Temp: %s C",
                     parts[0], parts[2], parts[1], parts[3], parts[4])
    except Exception:
        pass

    log.info("Forcing NVIDIA GPU (CUDA_VISIBLE_DEVICES=0)")
    log.info("Resource limits: GPU layers=%d, ctx=%d, threads=%d, low_vram=True",
             OLLAMA_OPTIONS["num_gpu"], OLLAMA_OPTIONS["num_ctx"], OLLAMA_OPTIONS["num_thread"])

    print()
    print("=" * 60)
    print("  JODI PREDICTION FOR WEEK: 30/03/2026 - 04/04/2026")
    print("  (Sunday is holiday -- predicting MON through SAT)")
    print("  Model: {} | Methods: Statistical + LLM".format(MODEL))
    print("=" * 60)
    print()

    # Load data
    jodi_data = load_all_data()
    print()

    results = {}

    for day in DAYS:
        date = TARGET_WEEK[day]
        vals = jodi_data[day]

        print("-" * 60)
        print(f"  {day} ({date})")
        print("-" * 60)

        # Compute statistics
        stats = compute_statistics(vals)
        print(f"  History: {stats['count']} weeks | Last 5: {', '.join(f'{v:02d}' for v in stats['last_5'])}")
        print(f"  Recent mean: {stats['mean_recent_20']} | Odd ratio: {stats['odd_ratio_recent']:.0%}")

        # Statistical predictions
        stat_preds = statistical_predict(vals, stats)
        for sp in stat_preds:
            mname = sp['method'][:35].ljust(35)
            print(f"    [{mname}] -> {sp['prediction']:02d}  (conf {sp['confidence']:.0%})")

        # LLM deep prediction
        log.info("  %s: Calling LLM for deep analysis...", day)
        llm_result = llm_deep_predict(day, vals, stats)
        if llm_result["prediction"] is not None:
            print(f"    [{'LLM Deep Analysis':35s}] -> {llm_result['prediction']:02d}  (conf {llm_result['confidence']:.0%})")
            if llm_result.get("reasoning"):
                # Show last 2 sentences of reasoning
                sentences = llm_result["reasoning"].replace("\n", " ").split(".")
                brief = ". ".join(s.strip() for s in sentences[-3:] if s.strip())
                if brief:
                    print(f"      AI reasoning: ...{brief}")
        else:
            print(f"    [{'LLM Deep Analysis':35s}] -> FAILED")

        # Ensemble
        all_preds = stat_preds + [llm_result]
        best, conf = ensemble_vote(all_preds)
        results[day] = {"date": date, "prediction": best, "confidence": conf, "details": all_preds}

        print(f"  >>> ENSEMBLE PREDICTION: {best:02d} (confidence: {conf:.0%})")
        print()

    # ── Final Summary ──
    print()
    print("=" * 60)
    print("  FINAL PREDICTIONS: Week of 30/03/2026 to 04/04/2026")
    print("=" * 60)
    print()
    print(f"  {'Day':<5} {'Date':<12} {'Predicted':>10} {'Confidence':>12}")
    print(f"  {'---':<5} {'----':<12} {'---------':>10} {'----------':>12}")
    for day in DAYS:
        r = results[day]
        print(f"  {day:<5} {r['date']:<12} {r['prediction']:>8d}   {r['confidence']:>10.0%}")
    print()

    # Export to Excel
    try:
        rows = []
        for day in DAYS:
            r = results[day]
            detail_str = " | ".join(
                f"{p['method'][:25]}={p['prediction']:02d}" 
                for p in r["details"] if p.get("prediction") is not None
            )
            rows.append({
                "Day": day,
                "Date": r["date"],
                "Predicted Jodi": r["prediction"],
                "Confidence": f"{r['confidence']:.0%}",
                "Method Breakdown": detail_str,
            })
        df = pd.DataFrame(rows)
        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as w:
            df.to_excel(w, sheet_name="Predictions", index=False)
        log.info("Results saved to 'Predictions' sheet in %s", EXCEL_FILE)
    except Exception as e:
        log.warning("Could not save to Excel: %s", e)

    print("Done! Check 'Predictions' sheet in Number_Chart.xlsx")
    print()


if __name__ == "__main__":
    main()
