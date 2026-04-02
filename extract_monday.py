import pandas as pd
df = pd.read_excel("Number_Chart.xlsx", sheet_name="Numeric Analysis")
mon = df["MON Jodi Num"].dropna().iloc[-20:].tolist()
print(f"Last 20 Mondays: {mon}")
