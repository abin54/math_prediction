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
    return mapping.get(day, 0)

def audit_week(start_date, end_date):
    print(f"--- QUANTUM BACKTRACK AUDIT: {start_date} to {end_date} ---")
    data = [
        {"date": "2026-04-01", "day": "Wednesday", "actual": 19, "open": 1, "close": 9},
        {"date": "2026-04-02", "day": "Thursday", "actual": 16, "open": 1, "close": 6},
        {"date": "2026-04-03", "day": "Friday", "actual": 50, "open": 5, "close": 0},
        {"date": "2026-04-04", "day": "Saturday", "actual": 26, "open": 2, "close": 6}
    ]
    
    for d in data:
        rt = get_root(d["date"])
        ld = get_lord(d["day"])
        # Offsets
        off_open = (d["open"] - (15 - rt - ld)) % 10
        # What logic would have predicted the Close?
        # Mirror: (Open + 5) % 10
        # Step: (Prev_Close + Delta) % 10
        mirror_val = (d["open"] + 5) % 10
        is_mirror = (d["close"] == mirror_val)
        
        print(f"Date: {d['date']} | Open: {d['open']} | Off: {off_open} | Close: {d['close']} (Mirror {mirror_val}? {is_mirror})")

    # Sequence Analysis
    opens = [d["open"] for d in data]
    closes = [d["close"] for d in data]
    print(f"\nOpen Sequence: {opens} | Diffs: {np.diff(opens)}")
    print(f"Close Sequence: {closes} | Diffs: {np.diff(closes)}")
    
    print("\n--- Forensic Result ---")
    print("1. Friday (50) was a PEAK Offset (+4).")
    print("2. Saturday (26) was a SUSTAINED Offset (+4).")
    print("3. Closes followed a FLIPPING symmetry: 6 -> 0 -> 6 (Thu, Fri, Sat).")
    print("   This implies Monday Close could be 0 (Flipping back) or 3 (Relative Similarity).")

if __name__ == "__main__":
    audit_week("2026-04-01", "2026-04-04")
