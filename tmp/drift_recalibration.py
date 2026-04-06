import pandas as pd
import numpy as np

def get_root(date_str):
    digits = [int(d) for d in str(date_str) if d.isdigit()]
    total = sum(digits)
    while total > 9:
        total = sum(int(d) for d in str(total))
    return total

def get_lord(day):
    mapping = {"Sunday": 1, "Monday": 2, "Tuesday": 9, "Wednesday": 5, "Thursday": 3, "Friday": 6, "Saturday": 8}
    return mapping[day]

# Data from CSV
history = [
    {"date": "2026-04-01", "day": "Wednesday", "open": 1},
    {"date": "2026-04-02", "day": "Thursday", "open": 1},
    {"date": "2026-04-03", "day": "Friday", "open": 5},
    {"date": "2026-04-04", "day": "Saturday", "open": 2}
]

offsets = []
print("--- Historical Offset Audit ---")
for h in history:
    root = get_root(h["date"])
    lord = get_lord(h["day"])
    offset = (h["open"] - (15 - root - lord)) % 10
    offsets.append(offset)
    print(f"Date: {h['date']} | Root: {root} | Lord: {lord} | Open: {h['open']} | OFFSET: {offset}")

# Drift Analysis
deltas = np.diff(offsets)
accel = np.diff(deltas)

v_last = deltas[-1]
a_last = accel[-1] if len(accel) > 0 else 0

# Predicted Next Offset
# Method 1: Velocity Persistence
v_next_1 = v_last
# Method 2: Acceleration Correction
v_next_2 = v_last + a_last

print("\n--- Drift Analysis ---")
print(f"Offsets: {offsets}")
print(f"Velocities (V): {deltas}")
print(f"Acceleration (A): {accel}")

# Today is Monday, 2026-04-06
root_mon = get_root("2026-04-06")
lord_mon = get_lord("Monday")

for v in set([v_next_1, v_next_2, -1, -4, 0]):
    off_pred = (offsets[-1] + v) % 10
    open_pred = (15 - root_mon - lord_mon + off_pred) % 10
    print(f"V_pred={v:+} -> Offset={off_pred} -> OPEN={open_pred}")

print("\n--- Forensic Socratic Audit ---")
print("If V repeats acceleration transition (V moves 0 -> +2), Offset=6, OPEN=7.")
print("If V repeats sequence trend (Average V = -1), Offset=3, OPEN=4.")
print("If V regresses to zero (Offset=0), OPEN=1.")
