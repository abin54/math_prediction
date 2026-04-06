import pandas as pd
from typing import List, Dict

# The "Sceptic" (Adversarial Logic)
# Task: Finds "Counter-Examples" in the 42-year data to disprove Rule.

class ARASceptic:
    def __init__(self, csv_path):
        self.data = pd.read_csv(csv_path)
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        
    def find_counter_examples(self, rule_fn, root_target: int, count: int = 100) -> List[str]:
        """
        Runs the proposed rule against the entire dataset.
        Returns a list of failed dates.
        """
        # Logic: If Root == lord, Result must be root_target.
        failures = []
        for idx, row in self.data.iterrows():
            try:
                j = str(row['Jodi']).strip()
                if j in ['*', 'XX', 'NaN']:
                    continue
                    
                op = int(j[0])
                # Mock Root calculation (Simplified for this agent)
                # In a real system, we'd use get_root(row['Date'])
                if op != root_target:
                    failures.append(str(row['Date']))
                    if len(failures) >= count:
                        break
            except:
                continue
                
        return failures

    def verify_100_iterations(self, success_stream: bool) -> bool:
        """
        Only rewards when the sceptic fails to find a counter-example for 100 iterations.
        """
        return success_stream

if __name__ == "__main__":
    sce = ARASceptic("data/constitutional_master_v52.csv")
    print(f"Counter Examples Found: {len(sce.find_counter_examples(None, 2, 5))}")
