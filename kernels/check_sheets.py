import pandas as pd
try:
    xl1 = pd.ExcelFile("Number_Chart.xlsx")
    print(f"Number_Chart.xlsx sheets: {xl1.sheet_names}")
except Exception as e:
    print(f"Error reading Number_Chart.xlsx: {e}")

try:
    xl2 = pd.ExcelFile("Kalyan_Panel_Chart_Dataset.xlsx")
    print(f"Kalyan_Panel_Chart_Dataset.xlsx sheets: {xl2.sheet_names}")
except Exception as e:
    print(f"Error reading Kalyan_Panel_Chart_Dataset.xlsx: {e}")
