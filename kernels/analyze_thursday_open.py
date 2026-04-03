import pandas as pd
df = pd.read_excel("Number_Chart.xlsx", sheet_name="Numeric Analysis")

# Extract the last 20 Thursdays and Wednesdays
thu = df["THU Jodi Num"].dropna().astype(int).tolist()[-20:]
wed = df["WED Jodi Num"].dropna().astype(int).tolist()[-20:]

print(f"Last 20 Wednesdays: {wed}")
print(f"Last 20 Thursdays:  {thu}")

# Analyze Open (Tens Digit)
wed_opens = [v // 10 for v in wed]
thu_opens = [v // 10 for v in thu]

print(f"Wed Opens: {wed_opens}")
print(f"Thu Opens: {thu_opens}")

# Count WED(1) -> THU(1) transitions
match_count = 0
for i in range(len(wed_opens)):
    if wed_opens[i] == 1 and thu_opens[i] == 1:
        match_count += 1
print(f"Matches for WED(1) -> THU(1): {match_count}")
