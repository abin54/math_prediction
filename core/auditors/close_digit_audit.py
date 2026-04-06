import pandas as pd
from core.hard_rules import HardRules

class CloseDigitAuditor:
    """
    Forensic Diagnostic: Identifying Close-Digit Symmetry Partner.
    Analyzes the 1974-2026 Friday-8 Close records.
    """
    
    def __init__(self, dataset_path: str = "data/constitutional_master_v52.csv"):
        self.data = pd.read_csv(dataset_path)
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.rules = HardRules()
        
    def analyze_friday_8_closes(self):
        """
        Scans all Friday-8 nodes for the Close-Digit Constant.
        """
        print("\n" + "="*80)
        print("  POST-MORTEM DIAGNOSTIC: FRIDAY-8 CLOSE-DIGIT SCAN")
        print("="*80)
        
        fridays = self.data[self.data['Date'].dt.day_name() == "Friday"]
        
        for _, row in fridays.iterrows():
            try:
                open_val = str(row['Open'])
                jodi = str(row['Jodi'])
                close_val = str(row['Close'])
                root = self.rules.get_numerological_value(row['Date'].strftime('%Y-%m-%d'))
                
                if root == 8:
                    if open_val == '3' or open_val == '5':
                        print(f"    - Node {row['Date'].date()}: Open {open_val} | Jodi {jodi} | Close {close_val}")
            except (ValueError, TypeError):
                continue
        
        print("="*80 + "\n")

if __name__ == "__main__":
    auditor = CloseDigitAuditor()
    auditor.analyze_friday_8_closes()
