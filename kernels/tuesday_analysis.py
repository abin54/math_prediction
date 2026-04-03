"""
Deep Tuesday Pattern Analysis — All Historical Data
Yesterday (MON) = 74, Predict today (TUE 31/03/2026)
"""
import sys, io, os
import pandas as pd
import numpy as np
from collections import Counter

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

os.chdir(r'f:\PROJECTS\MATH PREDICTION')
df = pd.read_excel('Number_Chart.xlsx', sheet_name='Numeric Analysis', header=0)

tue_vals = pd.to_numeric(df['TUE Jodi Num'], errors='coerce').dropna().astype(int).tolist()
mon_vals = pd.to_numeric(df['MON Jodi Num'], errors='coerce').dropna().astype(int).tolist()

YESTERDAY = 74

print("=" * 70)
print("  DEEP TUESDAY ANALYSIS - ALL HISTORICAL PATTERNS")
print("=" * 70)
print(f"\nTotal TUE data points: {len(tue_vals)}")
print(f"Total MON data points: {len(mon_vals)}")

# 1. MOST FREQUENT TUESDAY NUMBERS
print("\n" + "-" * 70)
print("  1. MOST FREQUENT TUESDAY JODI NUMBERS (ALL TIME)")
print("-" * 70)
c_all = Counter(tue_vals)
for v, cnt in c_all.most_common(15):
    pct = cnt / len(tue_vals) * 100
    bar = "#" * int(pct * 2)
    print(f"    {v:02d}: {cnt:3d} times ({pct:.1f}%) {bar}")

# 2. RECENT 30 TUESDAYS
print("\n" + "-" * 70)
print("  2. RECENT 30 TUESDAY VALUES")
print("-" * 70)
recent_30 = tue_vals[-30:]
for i in range(0, len(recent_30), 6):
    chunk = recent_30[i : i + 6]
    row = "  ".join(f"{v:02d}" for v in chunk)
    print(f"    {row}")

c_30 = Counter(recent_30)
print("\n  Most frequent in recent 30:")
for v, cnt in c_30.most_common(10):
    print(f"    {v:02d}: {cnt} times")

# 3. TENS & UNITS DISTRIBUTION
print("\n" + "-" * 70)
print("  3. TENS & UNITS DIGIT DISTRIBUTION (ALL TIME)")
print("-" * 70)
tens_c = Counter(v // 10 for v in tue_vals)
units_c = Counter(v % 10 for v in tue_vals)
print("  Tens digit:")
for d in range(10):
    cnt = tens_c.get(d, 0)
    print(f"    {d}: {cnt:3d} ({cnt / len(tue_vals) * 100:.1f}%)")
print("  Units digit:")
for d in range(10):
    cnt = units_c.get(d, 0)
    print(f"    {d}: {cnt:3d} ({cnt / len(tue_vals) * 100:.1f}%)")

# 4. WEEK-TO-WEEK DIFFERENCES
print("\n" + "-" * 70)
print("  4. WEEK-TO-WEEK DIFFERENCE PATTERN (LAST 20)")
print("-" * 70)
diffs = [tue_vals[i + 1] - tue_vals[i] for i in range(len(tue_vals) - 1)]
last_20_diffs = diffs[-20:]
for i, d in enumerate(last_20_diffs):
    src = tue_vals[-(21 - i)]
    dst = tue_vals[-(20 - i)]
    print(f"    {src:02d} -> {dst:02d}  (delta: {d:+d})")
print(f"  Avg delta (last 20): {np.mean(last_20_diffs):+.1f}")
print(f"  Median delta (last 20): {np.median(last_20_diffs):+.1f}")

# 5. MON->TUE TRANSITION when MON=74
print("\n" + "-" * 70)
print("  5. MON->TUE TRANSITION ANALYSIS (YESTERDAY=74)")
print("-" * 70)
min_len = min(len(mon_vals), len(tue_vals))
exact74 = []
tens7 = []
units4 = []
all_deltas = []
for i in range(min_len):
    all_deltas.append(tue_vals[i] - mon_vals[i])
    if mon_vals[i] == 74:
        exact74.append(tue_vals[i])
    if mon_vals[i] // 10 == 7:
        tens7.append(tue_vals[i])
    if mon_vals[i] % 10 == 4:
        units4.append(tue_vals[i])

print(f"  When MON was exactly 74 -> TUE was: {exact74}")
if exact74:
    print(f"    Most common: {Counter(exact74).most_common(5)}")

print(f"\n  When MON tens=7 ({len(tens7)} times) -> Top TUE:")
if tens7:
    for v, cnt in Counter(tens7).most_common(8):
        print(f"    {v:02d}: {cnt} times")

print(f"\n  When MON units=4 ({len(units4)} times) -> Top TUE:")
if units4:
    for v, cnt in Counter(units4).most_common(8):
        print(f"    {v:02d}: {cnt} times")

print(f"\n  MON->TUE delta stats:")
print(f"    Mean: {np.mean(all_deltas):+.1f}")
print(f"    Median: {np.median(all_deltas):+.1f}")
print(f"    Recent 5: {all_deltas[-5:]}")

# 6. TUESDAY SELF-FOLLOW PATTERNS
print("\n" + "-" * 70)
print("  6. TUESDAY SELF-FOLLOW PATTERNS")
print("-" * 70)
last_tue = tue_vals[-1]
print(f"  Last TUE value: {last_tue:02d}")
followers_exact = []
followers_tens = []
followers_units = []
for i in range(len(tue_vals) - 1):
    if tue_vals[i] == last_tue:
        followers_exact.append(tue_vals[i + 1])
    if tue_vals[i] // 10 == last_tue // 10:
        followers_tens.append(tue_vals[i + 1])
    if tue_vals[i] % 10 == last_tue % 10:
        followers_units.append(tue_vals[i + 1])

print(f"  After TUE={last_tue:02d} exactly: {followers_exact}")
if followers_exact:
    print(f"    Most common: {Counter(followers_exact).most_common(5)}")
print(f"\n  After TUE tens={last_tue // 10} ({len(followers_tens)} times):")
if followers_tens:
    for v, cnt in Counter(followers_tens).most_common(8):
        print(f"    {v:02d}: {cnt} times")
print(f"\n  After TUE units={last_tue % 10} ({len(followers_units)} times):")
if followers_units:
    for v, cnt in Counter(followers_units).most_common(8):
        print(f"    {v:02d}: {cnt} times")

# 7. PARITY PATTERNS
print("\n" + "-" * 70)
print("  7. PARITY PATTERNS (LAST 20 TUESDAYS)")
print("-" * 70)
last20 = tue_vals[-20:]
for v in last20:
    t = v // 10
    u = v % 10
    parity = "EVEN" if v % 2 == 0 else "ODD"
    tp = "E" if t % 2 == 0 else "O"
    up = "E" if u % 2 == 0 else "O"
    print(f"    {v:02d}  tens={t}({tp}) units={u}({up})  {parity}")

even_cnt = sum(1 for v in last20 if v % 2 == 0)
odd_cnt = 20 - even_cnt
print(f"\n  Even: {even_cnt}/20, Odd: {odd_cnt}/20")
is_even = "EVEN" if last_tue % 2 == 0 else "ODD"
print(f"  Last value {last_tue:02d} is {is_even}")

# 8. REPEATING / CYCLE ANALYSIS
print("\n" + "-" * 70)
print("  8. GAP/CYCLE ANALYSIS - NUMBERS OVERDUE")
print("-" * 70)
last_seen = {}
for i, v in enumerate(tue_vals):
    last_seen[v] = i
current_idx = len(tue_vals) - 1
gaps = {v: current_idx - idx for v, idx in last_seen.items()}
overdue = sorted(gaps.items(), key=lambda x: -x[1])[:15]
print("  Most overdue numbers:")
for v, g in overdue:
    print(f"    {v:02d}: last seen {g} weeks ago")

# 9. SUM DIGIT ANALYSIS
print("\n" + "-" * 70)
print("  9. DIGIT SUM PATTERNS (LAST 20)")
print("-" * 70)
for v in last20:
    dsum = (v // 10) + (v % 10)
    print(f"    {v:02d} -> digit sum = {dsum}")
dsums = [(v // 10) + (v % 10) for v in last20]
print(f"\n  Avg digit sum (last 20): {np.mean(dsums):.1f}")
print(f"  Most common digit sums: {Counter(dsums).most_common(5)}")

# 10. FINAL CONSOLIDATED PREDICTION
print("\n" + "=" * 70)
print("  10. CONSOLIDATED PREDICTION LOGIC")
print("=" * 70)

# Collect candidates from each method
candidates = Counter()

# From frequency (recent 30)
for v, cnt in c_30.most_common(5):
    candidates[v] += cnt * 3  # weight by frequency

# From MON=74 exact followers
for v in exact74:
    candidates[v] += 15  # strong signal

# From MON tens=7 followers
for v, cnt in Counter(tens7).most_common(5):
    candidates[v] += cnt * 2

# From MON units=4 followers
for v, cnt in Counter(units4).most_common(5):
    candidates[v] += cnt

# From TUE self-follow (after last value)
for v in followers_exact:
    candidates[v] += 10

for v, cnt in Counter(followers_tens).most_common(5):
    candidates[v] += cnt

for v, cnt in Counter(followers_units).most_common(5):
    candidates[v] += cnt

# Delta based prediction
avg_delta = np.mean(all_deltas[-10:])
delta_pred = (YESTERDAY + int(round(avg_delta))) % 100
if delta_pred < 0:
    delta_pred += 100
candidates[delta_pred] += 8

# WMA prediction
recent_5 = tue_vals[-5:]
weights = [1, 2, 3, 4, 5]
wma = sum(v * w for v, w in zip(recent_5, weights)) / sum(weights)
tue_diffs = [tue_vals[i+1] - tue_vals[i] for i in range(len(tue_vals)-1)]
trend = np.mean(tue_diffs[-10:])
wma_pred = int(round(wma + trend)) % 100
if wma_pred < 0:
    wma_pred += 100
candidates[wma_pred] += 5

# Diff extrapolation
last_diff = tue_diffs[-1]
diff_pred = (tue_vals[-1] + last_diff) % 100
if diff_pred < 0:
    diff_pred += 100
candidates[diff_pred] += 4

print("\n  Top weighted candidates:")
for rank, (v, w) in enumerate(candidates.most_common(10)):
    marker = " >>>" if rank == 0 else "    "
    print(f"  {marker} {v:02d}  (weight: {w})")

print("\n" + "=" * 70)
top4 = candidates.most_common(4)
print(f"\n  *** TODAY'S TUESDAY PREDICTION (MON was 74) ***")
print(f"\n  1st Choice: {top4[0][0]:02d}  (weight: {top4[0][1]})")
if len(top4) > 1:
    print(f"  2nd Choice: {top4[1][0]:02d}  (weight: {top4[1][1]})")
if len(top4) > 2:
    print(f"  3rd Choice: {top4[2][0]:02d}  (weight: {top4[2][1]})")
if len(top4) > 3:
    print(f"  4th Choice: {top4[3][0]:02d}  (weight: {top4[3][1]})")
print("\n" + "=" * 70)
