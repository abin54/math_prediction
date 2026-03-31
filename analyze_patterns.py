import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import pandas as pd
import numpy as np
from collections import Counter

df = pd.read_excel('Number_Chart.xlsx', sheet_name='Numeric Analysis', header=0)
days = ['MON','TUE','WED','THU','FRI','SAT']

all_jodi = []
per_day = {}
for day in days:
    col = f'{day} Jodi Num'
    vals = pd.to_numeric(df[col], errors='coerce').dropna().astype(int).tolist()
    per_day[day] = vals
    all_jodi.extend(vals)

print(f'Total Jodi values across all days: {len(all_jodi)}')
print(f'Unique values: {len(set(all_jodi))}')
print(f'Range: {min(all_jodi)} to {max(all_jodi)}')

# FREQUENCY DISTRIBUTION
print('\n===== TOP 20 MOST FREQUENT JODI NUMBERS (ALL DAYS) =====')
c = Counter(all_jodi)
for val, cnt in c.most_common(20):
    bar = '#' * cnt
    print(f'  {val:02d} -> {cnt:3d} times  {bar}')

print('\n===== LEAST FREQUENT (BOTTOM 10) =====')
for val, cnt in c.most_common()[-10:]:
    print(f'  {val:02d} -> {cnt:3d} times')

# TENS DIGIT AND UNITS DIGIT DISTRIBUTION
tens = [v // 10 for v in all_jodi]
units = [v % 10 for v in all_jodi]
print('\n===== TENS DIGIT FREQUENCY =====')
tc = Counter(tens)
for d in range(10):
    cnt = tc.get(d, 0)
    print(f'  {d}: {cnt} ({cnt/len(all_jodi)*100:.1f}%)')

print('\n===== UNITS DIGIT FREQUENCY =====')
uc = Counter(units)
for d in range(10):
    cnt = uc.get(d, 0)
    print(f'  {d}: {cnt} ({cnt/len(all_jodi)*100:.1f}%)')

# DAY-TO-DAY TRANSITIONS (within same week)
print('\n===== DAY-TO-DAY TRANSITIONS (within same week) =====')
for i in range(len(days)-1):
    d1, d2 = days[i], days[i+1]
    v1 = per_day[d1]
    v2 = per_day[d2]
    mn = min(len(v1), len(v2))
    diffs = [v2[j] - v1[j] for j in range(mn)]
    print(f'  {d1}->{d2}: avg change={np.mean(diffs):.1f}, std={np.std(diffs):.1f}, median change={np.median(diffs):.0f}')

# WEEK-TO-WEEK (same day)
print('\n===== WEEK-TO-WEEK TRANSITIONS (same day, consecutive weeks) =====')
for day in days:
    vals = per_day[day]
    diffs = [vals[i+1] - vals[i] for i in range(len(vals)-1)]
    print(f'  {day}: avg change={np.mean(diffs):.1f}, std={np.std(diffs):.1f}')

# AUTOCORRELATION
print('\n===== AUTOCORRELATION (SAME DAY, lag 1-5) =====')
for day in days:
    vals = np.array(per_day[day], dtype=float)
    if len(vals) < 10:
        continue
    acorrs = []
    for lag in range(1, 6):
        corr = np.corrcoef(vals[:-lag], vals[lag:])[0, 1]
        acorrs.append(f'lag{lag}={corr:.3f}')
    print(f'  {day}: {"  ".join(acorrs)}')

# REPEATING PATTERNS
print('\n===== REPEAT ANALYSIS (same Jodi on consecutive weeks, same day) =====')
for day in days:
    vals = per_day[day]
    repeats = sum(1 for i in range(len(vals)-1) if vals[i] == vals[i+1])
    print(f'  {day}: {repeats} exact repeats out of {len(vals)-1} transitions ({repeats/(len(vals)-1)*100:.1f}%)')

# GAP ANALYSIS — how many weeks before a number reappears
print('\n===== AVG GAP (weeks between same number reappearing, same day) =====')
for day in days:
    vals = per_day[day]
    last_seen = {}
    gaps = []
    for i, v in enumerate(vals):
        if v in last_seen:
            gaps.append(i - last_seen[v])
        last_seen[v] = i
    print(f'  {day}: avg gap = {np.mean(gaps):.1f} weeks, median = {np.median(gaps):.0f} weeks')

# DIGIT SUM PATTERNS (since Jodi = digit sums)
print('\n===== JODI DIGIT SUM -> NEXT JODI CORRELATION =====')
for day in days:
    vals = per_day[day]
    # digit sum of jodi itself
    dsums = [(v // 10 + v % 10) for v in vals]
    next_vals = vals[1:]
    dsums_cur = dsums[:-1]
    corr = np.corrcoef(dsums_cur, next_vals)[0, 1]
    print(f'  {day}: corr(digitsum_jodi[t], jodi[t+1]) = {corr:.3f}')

# CROSS-DAY CORRELATION within same week (does MON predict TUE?)
print('\n===== CROSS-DAY CORRELATION (same week) =====')
for i in range(len(days)):
    for j in range(i+1, len(days)):
        d1, d2 = days[i], days[j]
        v1 = per_day[d1]
        v2 = per_day[d2]
        mn = min(len(v1), len(v2))
        corr = np.corrcoef(v1[:mn], v2[:mn])[0, 1]
        if abs(corr) > 0.05:
            print(f'  {d1} vs {d2}: corr = {corr:.3f}')
    
# ODD/EVEN PATTERN
print('\n===== ODD/EVEN SEQUENCE ANALYSIS (same day) =====')
for day in days:
    vals = per_day[day]
    oe = ['O' if v % 2 == 1 else 'E' for v in vals]
    # Check if odd follows odd, even follows even etc.
    transitions = Counter()
    for i in range(len(oe)-1):
        transitions[(oe[i], oe[i+1])] += 1
    total = len(oe) - 1
    for k in [('E','E'), ('E','O'), ('O','E'), ('O','O')]:
        cnt = transitions.get(k, 0)
        pct = cnt/total*100
        print(f'  {day}: {k[0]}->{k[1]}: {cnt} ({pct:.1f}%)')

# MOST COMMON PAIRS (consecutive jodi values, same day)
print('\n===== MOST COMMON CONSECUTIVE PAIRS (same day, top 5 each) =====')
for day in days:
    vals = per_day[day]
    pairs = [(vals[i], vals[i+1]) for i in range(len(vals)-1)]
    pc = Counter(pairs)
    print(f'  {day}:')
    for (a, b), cnt in pc.most_common(5):
        print(f'    {a:02d} -> {b:02d}  ({cnt} times)')

# LAST 10 VALUES for each day
print('\n===== LAST 10 JODI VALUES PER DAY =====')
for day in days:
    vals = per_day[day]
    last10 = vals[-10:]
    print(f'  {day}: {", ".join(f"{v:02d}" for v in last10)}')
