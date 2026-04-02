
import pandas as pd
from collections import Counter

EXCEL_FILE = "Number_Chart.xlsx"

def analyze_sums():
    df = pd.read_excel(EXCEL_FILE, sheet_name="Numeric Analysis")
    mon = df["MON Jodi Num"].dropna().astype(int).tolist()
    tue = df["TUE Jodi Num"].dropna().astype(int).tolist()
    wed = df["WED Jodi Num"].dropna().astype(int).tolist()
    thu = df["THU Jodi Num"].dropna().astype(int).tolist()
    
    min_len = min(len(mon), len(tue), len(wed))
    
    def get_sum(n):
        return (n // 10 + n % 10) % 10
    
    current_sums = [get_sum(74), get_sum(4), get_sum(19)]
    print(f"Current Sums this week: {current_sums}") # [1, 4, 0]
    
    sum_matches = []
    for i in range(min_len):
        s1 = get_sum(mon[i])
        s2 = get_sum(tue[i])
        s3 = get_sum(wed[i])
        if s1 == current_sums[0] and s2 == current_sums[1] and s3 == current_sums[2]:
            t_sum = get_sum(thu[i]) if i < len(thu) else "???"
            t_val = thu[i] if i < len(thu) else "???"
            sum_matches.append((i, t_val, t_sum))
            
    print(f"\nHistorical weeks with Sum sequence 1 -> 4 -> 0: {len(sum_matches)}")
    for idx, val, s_val in sum_matches:
        print(f" - Week {idx}: MON={mon[idx]:02d}, TUE={tue[idx]:02d}, WED={wed[idx]:02d} -> THU: {val:02d} (Sum={s_val})")

    if sum_matches:
        next_vals = [v for i, v, s in sum_matches]
        next_sums = [s for i, v, s in sum_matches]
        print(f"\nStatistical Conclusion for Thursday:")
        print(f"Most common Sum on THU: {Counter(next_sums).most_common(1)}")
        print(f"Most common Jodi on THU: {Counter(next_vals).most_common(1)}")

if __name__ == "__main__":
    analyze_sums()
