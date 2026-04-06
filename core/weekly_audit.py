import pandas as pd
from core.hard_rules import HardRules

def run_weekly_symmetry_audit():
    print("\n" + "="*80)
    print("  WEEKLY SYMMETRY AUDIT: THE 52-YEAR CONSTITUTIONAL RECORD")
    print("="*80)
    
    data = pd.read_csv("data/constitutional_master_v52.csv")
    data['Date'] = pd.to_datetime(data['Date'])
    rules = HardRules()
    
    # Calculate Root and Match for every entry
    results = []
    for _, row in data.iterrows():
        try:
            actual = int(row['Open'])
            root = rules.get_numerological_value(row['Date'].strftime('%Y-%m-%d'))
            # Match types: Direct (Root == Open) or Harmonic (Sum = 10)
            direct = (actual == root)
            harmonic = ((actual + root) % 10 == 0)
            results.append({"Date": row['Date'], "Match": (direct or harmonic)})
        except (ValueError, TypeError):
            continue
            
    df_audit = pd.DataFrame(results)
    
    # Check by Year
    print("\n  [Dataset Scan] Multi-Decadal Consistency:")
    for year in range(1972, 2030, 8): # 8-year cycles
        end_year = year + 7
        mask = (df_audit['Date'].dt.year >= year) & (df_audit['Date'].dt.year <= end_year)
        if df_audit[mask].empty: continue
        score = df_audit[mask]['Match'].mean() * 100
        print(f"    - Cycle {year}-{end_year}: {score:.2f}% Rule Resonance")
        
    total_score = df_audit['Match'].mean() * 100
    print(f"\n  [Grand Total] 19,816-Day Forensic Consistency: {total_score:.2f}%")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_weekly_symmetry_audit()
