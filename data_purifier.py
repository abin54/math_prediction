"""
Multi-Source Data Purifier v1.0
==============================
Cross-verifies results between Number_Chart and Panel_Chart.
Prevents Data-Corruption from ruining the 14-year scan.
"""

import pandas as pd
import numpy as np
import os, json

def verify_latest_state():
    print("    [PURIFIER] Cross-verifying Number_Chart vs Panel_Chart...")
    
    # 1. Load Number_Chart.xlsx
    df1 = pd.read_excel("Number_Chart.xlsx", sheet_name="Numeric Analysis")
    last_val_1 = df1["WED Jodi Num"].dropna().iloc[-1]
    
    # 2. Load Kalyan_Panel_Chart_Dataset.xlsx
    df2 = pd.read_excel("Kalyan_Panel_Chart_Dataset.xlsx")
    last_val_2 = df2[df2["Day"] == "Wed"]["Jodi"].dropna().iloc[-1]
    
    if int(last_val_1) != int(last_val_2):
        print(f"    [CRITICAL ERROR] Data Mismatch: {last_val_1} != {last_val_2}")
        return False
        
    print(f"    [SUCCESS] Data Sources Consistent (Wednesday={int(last_val_1)})")
    return True

if __name__ == "__main__":
    verify_latest_state()
