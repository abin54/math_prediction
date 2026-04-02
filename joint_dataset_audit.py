import pandas as pd
import numpy as np
from collections import Counter

def standardize_day(s):
    s = str(s).strip().upper()
    if s.startswith('MON'): return 'MON'
    if s.startswith('TUE'): return 'TUE'
    if s.startswith('WED'): return 'WED'
    if s.startswith('THU'): return 'THU'
    if s.startswith('FRI'): return 'FRI'
    if s.startswith('SAT'): return 'SAT'
    return s

def run_joint_audit():
    # DATASET 1: Number_Chart.xlsx (Historical 1972-2026)
    print("\n--- ANALYZING DATASET 1: Number_Chart.xlsx ---")
    df1 = pd.read_excel('Number_Chart.xlsx', sheet_name='Numeric Analysis')
    wed1 = df1['WED Jodi Num'].dropna().astype(int)
    open1_wed1 = wed1[wed1 // 10 == 1]
    print(f"  Dataset 1 Leader (Open 1): {open1_wed1.value_counts().head(3).to_dict()}")
    
    tue4_wed1 = df1[df1['TUE Jodi Num'] == 4]['WED Jodi Num'].dropna().astype(int)
    print(f"  Dataset 1 Followers (TUE 04): {tue4_wed1.value_counts().to_dict()}")

    # DATASET 2: Kalyan_Panel_Chart_Dataset.xlsx (Detailed)
    print("\n--- ANALYZING DATASET 2: Kalyan_Panel_Chart_Dataset.xlsx ---")
    df2 = pd.read_excel('Kalyan_Panel_Chart_Dataset.xlsx')
    df2['Day'] = df2['Day'].apply(standardize_day)
    df2['Open'] = pd.to_numeric(df2['Open'], errors='coerce')
    df2['Close'] = pd.to_numeric(df2['Close'], errors='coerce')
    df2 = df2.dropna(subset=['Open', 'Close', 'Day'])
    df2['Jodi'] = (df2['Open'] * 10 + df2['Close']).astype(int)
    
    # WED Open 1 in Dataset 2
    wed2_open1 = df2[(df2['Day'] == 'WED') & (df2['Open'] == 1)]['Jodi']
    print(f"  Dataset 2 Leader (Open 1): {wed2_open1.value_counts().head(3).to_dict()}")
    
    # Path TUE 04 -> WED in Dataset 2
    # Find indices of TUE 04
    tue04_idx = df2[(df2['Day'] == 'TUE') & (df2['Open'] == 0) & (df2['Close'] == 4)].index
    wed_after_04 = []
    for idx in tue04_idx:
        if idx + 1 < len(df2):
            next_row = df2.iloc[df2.index.get_loc(idx) + 1]
            if next_row['Day'] == 'WED':
                wed_after_04.append(int(next_row['Jodi']))
    print(f"  Dataset 2 Followers (TUE 04): {Counter(wed_after_04)}")

if __name__ == "__main__":
    run_joint_audit()
