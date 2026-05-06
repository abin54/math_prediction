import pandas as pd
from datetime import datetime

# New data from web
data = [
    ["01/04/2026", "Wednesday", 678, 19, 126],
    ["02/04/2026", "Thursday", 678, 16, 150],
    ["03/04/2026", "Friday", 889, 50, 370],
    ["04/04/2026", "Saturday", 138, 26, 240],
    ["06/04/2026", "Monday", 159, 51, 560],
    ["07/04/2026", "Tuesday", 278, 76, 457],
    ["08/04/2026", "Wednesday", 780, 56, 367],
    ["09/04/2026", "Thursday", 267, 51, 380],
    ["10/04/2026", "Friday", 180, 96, 150],
    ["11/04/2026", "Saturday", 679, 28, 468],
    ["13/04/2026", "Monday", 788, 30, 190],
    ["14/04/2026", "Tuesday", 460, "03", 229],
    ["15/04/2026", "Wednesday", 458, 77, 269],
    ["16/04/2026", "Thursday", 140, 53, 799],
    ["17/04/2026", "Friday", 279, 89, 469],
    ["18/04/2026", "Saturday", 490, 33, 120],
    ["20/04/2026", "Monday", 348, 53, 148],
    ["21/04/2026", "Tuesday", 690, 52, 480],
    ["22/04/2026", "Wednesday", 455, 48, 459],
    ["23/04/2026", "Thursday", 479, "04", 220],
    ["24/04/2026", "Friday", 468, 83, 256],
    ["25/04/2026", "Saturday", 269, 79, 450],
    ["27/04/2026", "Monday", 179, 79, 135],
    ["28/04/2026", "Tuesday", 469, 98, 224],
    ["29/04/2026", "Wednesday", 890, 75, 348],
    ["30/04/2026", "Thursday", 256, 37, 269],
    ["01/05/2026", "Friday", 180, 97, 250],
    ["02/05/2026", "Saturday", 123, 68, 459],
    ["04/05/2026", "Monday", 180, 95, 339],
    ["05/05/2026", "Tuesday", 137, 13, 148]
]

def calculate_digit(panna):
    return sum(int(d) for d in str(panna)) % 10

# Load existing data
file_path = "Kalyan_Panel_Chart_Dataset.xlsx"
df = pd.read_excel(file_path)

# Prepare new rows
new_rows = []
for row in data:
    date_str, day, open_panna, jodi, close_panna = row
    jodi_str = str(jodi).zfill(2)
    open_digit = int(jodi_str[0])
    close_digit = int(jodi_str[1])
    
    new_rows.append({
        "Date": date_str,
        "Day": day[:3], # Mon, Tue, etc.
        "Open": float(open_digit),
        "Close": float(close_digit),
        "Jodi": float(jodi),
        "Panel (Patti)": float(open_panna)
    })

new_df = pd.DataFrame(new_rows)

# Remove existing entries for these dates to avoid duplicates if re-running
existing_dates = set(df['Date'].astype(str))
new_df = new_df[~new_df['Date'].astype(str).isin(existing_dates)]

# Concatenate
updated_df = pd.concat([df, new_df], ignore_index=True)

# Save back to Excel
updated_df.to_excel(file_path, index=False)
print(f"Updated {len(new_df)} new rows in {file_path}")
