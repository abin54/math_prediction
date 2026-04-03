
import pandas as pd
import numpy as np

EXCEL_FILE = "Number_Chart.xlsx"

def diagnostic_audit():
    df = pd.read_excel(EXCEL_FILE, sheet_name="Numeric Analysis")
    
    mon = df["MON Jodi Num"].dropna().astype(int).tolist()
    tue = df["TUE Jodi Num"].dropna().astype(int).tolist()
    wed = df["WED Jodi Num"].dropna().astype(int).tolist()
    thu = df["THU Jodi Num"].dropna().astype(int).tolist()
    
    min_len = min(len(mon), len(tue), len(wed), len(thu))
    
    print("--- DIAGNOSTIC AUDIT: THE 1-OPEN ANOMALY (FIXED) ---")
    
    # 7 -> 0 -> 1 -> 1 logic
    seq_hits = []
    for i in range(min_len):
        o1, o2, o3, o4 = mon[i]//10, tue[i]//10, wed[i]//10, thu[i]//10
        if o1 == 7 and o2 == 0 and o3 == 1:
            seq_hits.append(i)
            
    print(f"\nWeeks starting with OPEN 7, 0, 1: {len(seq_hits)}")
    for idx in seq_hits:
        print(f" - Week {idx}: {mon[idx]:02d}, {tue[idx]:02d}, {wed[idx]:02d} -> THU: {thu[idx]:02d}")

    # Check for WED 1-Open -> THU 1-Open in the last 100 weeks
    print("\n[Recent 100 Weeks Mirror Anchor (1-1 Repeat)]:")
    repeat_1 = 0
    for i in range(min_len - 100, min_len):
        if wed[i]//10 == 1 and thu[i]//10 == 1:
            repeat_1 += 1
            print(f" - Week {i}: WED {wed[i]:02d} -> THU {thu[i]:02d}")
            
    # Check for Purnima (starting on Wednesday) specifically
    # April 1st was Purnima start.
    # April 2nd is Purnima.
    
    # Conclusion logic:
    # Historically, if Wednesday is 19, what is Thursday?
    target_followers = [thu[i] for i in range(min_len) if wed[i] == 19]
    print(f"\nFollowers of WED 19: {target_followers}")

if __name__ == "__main__":
    diagnostic_audit()
