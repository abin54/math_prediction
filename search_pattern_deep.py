
import pandas as pd

EXCEL_FILE = "Number_Chart.xlsx"
SHEET_NAME = "Numeric Analysis"

def search_week_pattern():
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    
    # Extract columns
    mon = df["MON Jodi Num"].dropna().astype(int).tolist()
    tue = df["TUE Jodi Num"].dropna().astype(int).tolist()
    wed = df["WED Jodi Num"].dropna().astype(int).tolist()
    thu = df["THU Jodi Num"].dropna().astype(int).tolist()
    
    min_len = min(len(mon), len(tue), len(wed))
    
    current_mon = 74
    current_tue = 4 # 04
    current_wed = 19
    
    print(f"Searching for historical weeks with similar start: MON={current_mon}, TUE={current_tue}, WED={current_wed}")
    
    matches_mon_tue = []
    matches_all_three = []
    
    for i in range(min_len):
        if mon[i] == current_mon and tue[i] == current_tue:
            matches_mon_tue.append(i)
            if wed[i] == current_wed:
                matches_all_three.append(i)
                
    print(f"\nWeeks starting with 74 (MON) -> 04 (TUE): {len(matches_mon_tue)}")
    for idx in matches_mon_tue:
        w_vals = [mon[idx], tue[idx], wed[idx]]
        t_val = thu[idx] if idx < len(thu) else "???"
        print(f" - Week {idx}: {w_vals} -> THU: {t_val}")
        
    print(f"\nWeeks starting with 74 (MON) -> 04 (TUE) -> 19 (WED): {len(matches_all_three)}")
    for idx in matches_all_three:
        t_val = thu[idx] if idx < len(thu) else "???"
        print(f" - Match Index {idx} -> THU: {t_val}")

    # Check for "Family" matches or "Mirror" matches
    # Current trend: Open (7->0->1), Close (4->4->9)
    # 7->0 (+3), 0->1 (+1)
    # 4->4 (0), 4->9 (+5)
    
    print("\n--- Pattern Match (Steps) ---")
    for i in range(1, min_len):
        # Open steps
        o1 = mon[i] // 10
        o2 = tue[i] // 10
        o3 = wed[i] // 10
        
        # Close steps
        c1 = mon[i] % 10
        c2 = tue[i] % 10
        c3 = wed[i] % 10
        
        # Check if steps match: (7->0, 0->1) is (-7, +1)
        # (4->4, 4->9) is (0, +5)
        
        o_step1 = (o2 - o1) % 10
        o_step2 = (o3 - o2) % 10
        c_step1 = (c2 - c1) % 10
        c_step2 = (c3 - c2) % 10
        
        if o_step1 == 3 and o_step2 == 1 and c_step1 == 0 and c_step2 == 5:
            t_val = thu[i] if i < len(thu) else "???"
            print(f" - STEP MATCH found at index {i}: MON={mon[i]:02d}, TUE={tue[i]:02d}, WED={wed[i]:02d} -> THU: {t_val}")

if __name__ == "__main__":
    search_week_pattern()
