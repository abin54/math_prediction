
import pandas as pd
import os

EXCEL_FILE = "Number_Chart.xlsx"
SHEET_NAME = "Numeric Analysis"
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]

def check_data():
    if not os.path.exists(EXCEL_FILE):
        print(f"Error: {EXCEL_FILE} not found.")
        return

    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
        print(f"Latest Data from {EXCEL_FILE}:")
        print("-" * 30)
        for day in DAYS:
            col = f"{day} Jodi Num"
            if col in df.columns:
                vals = df[col].dropna().astype(int).tolist()
                last_5 = vals[-5:] if len(vals) >= 5 else vals
                print(f"{day}: {last_5}")
            else:
                print(f"{day}: Column not found")
    except Exception as e:
        print(f"Error reading Excel: {e}")

if __name__ == "__main__":
    check_data()
