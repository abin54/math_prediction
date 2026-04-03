
import pandas as pd
import numpy as np

EXCEL_FILE = "Number_Chart.xlsx"

def diagnostic_audit():
    df = pd.read_excel(EXCEL_FILE, sheet_name="Numeric Analysis")
    
    # This Week: MON 74, TUE 04, WED 19, THU 1-Open
    # Target: Why did THU open with 1?
    
    mon = df["MON Jodi Num"].dropna().astype(int).tolist()
    tue = df["TUE Jodi Num"].dropna().astype(int).tolist()
    wed = df["WED Jodi Num"].dropna().astype(int).tolist()
    thu = df["THU Jodi Num"].dropna().astype(int).tolist()
    
    min_len = min(len(mon), len(tue), len(wed), len(thu))
    
    print("--- DIAGNOSTIC AUDIT: THE 1-OPEN ANOMALY ---")
    print(f"Goal: Find historical weeks where THU starts with 1 following WED 19 or similar patterns.")
    
    # Pattern 1: Exact Wednesday 19 -> Thursday Open 1
    exact_matches = []
    for i in range(min_len):
        if wed[i] == 19 and thu[i] // 10 == 1:
            matches.append(i) # wait, typo in my script
            
    # Pattern 2: Triple-Digit-Sum Echo
    # MON 74 (Sum 1), TUE 04 (Sum 4), WED 19 (Sum 10 -> 0)
    # Why is THU Open 1?
    # Maybe Sum of WED Open + THU Open? 1 + 1 = 2?
    
    # Pattern 3: The "Date" Logic
    # April 2 -> 2. Jupiter -> 3. Year -> 1.
    
    print("\n[Deep Dataset Search]:")
    total_1_open_thu = 0
    pattern_hits = []
    for i in range(min_len):
        # Did Wednesday Open 1 result in Thursday Open 1?
        if wed[i] // 10 == 1 and thu[i] // 10 == 1:
            total_1_open_thu += 1
            pattern_hits.append((i, mon[i], tue[i], wed[i], thu[i]))
            
    print(f"Found {total_1_open_thu} instances of Double-Open 1 on WED-THU.")
    for idx, m, t, w, th in pattern_hits[-5:]:
        print(f" - Week {idx}: MON {m:02d}, TUE {t:02d}, WED {w:02d} -> THU {th:02d}")

    # Analyzing the "Missing Logic":
    # Let's check the distance between Wednesday and Thursday Open
    # If Wednesday was 1, and Thursday is 1, distance is 0.
    
    # 52-Year Purnima Alignment
    # Does Purnima usually trigger a "Repeat" digit?
    # Purnima is Today. Yesterday was Purnima start.
    
    # What was the result of WED 19 in history?
    print("\n[Followers of WED 19 on Thursday]:")
    f19 = [thu[i] for i in range(min_len) if wed[i] == 19]
    print(f"Jodis: {f19}")

if __name__ == "__main__":
    diagnostic_audit()
