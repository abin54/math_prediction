from typing import List, Optional
import pandas as pd
from core.utils.path_manager import PathManager
from core.utils.logger import sovereign_logger as logger

class ARASceptic:
    """
    The 'Sceptic' Agent: Performs adversarial logic validation.
    Searches for counter-examples in historical datasets to stress-test rules.
    """
    
    def __init__(self, dataset_name: str = "constitutional_master_v52.csv"):
        self.csv_path = PathManager.get_data_path(dataset_name)
        self._load_data()
        
    def _load_data(self):
        """Loads and prepares the historical dataset."""
        try:
            self.data = pd.read_csv(self.csv_path)
            self.data['Date'] = pd.to_datetime(self.data['Date'])
            logger.info(f"ARASceptic: Loaded {len(self.data)} historical records from {self.csv_path.name}")
        except Exception as e:
            logger.error(f"Failed to load dataset for Sceptic: {e}")
            self.data = pd.DataFrame()

    def find_counter_examples(self, root_target: int, limit: int = 100) -> List[str]:
        """
        Runs the proposed rule against the entire dataset to find logical failures.
        
        Args:
            root_target: The target numerical root to validate.
            limit: Maximum number of counter-examples to return.
            
        Returns:
            A list of dates where the logic failed.
        """
        if self.data.empty:
            logger.warning("ARASceptic: No data available for validation.")
            return []

        failures = []
        for _, row in self.data.iterrows():
            try:
                jodi = str(row.get('Jodi', '')).strip()
                if jodi in ['*', 'XX', 'NaN', '']:
                    continue
                    
                open_digit = int(jodi[0])
                # Logical Test: If the open digit doesn't match the root_target, it's a potential failure
                if open_digit != root_target:
                    failures.append(str(row['Date']))
                    if len(failures) >= limit:
                        break
            except (ValueError, IndexError) as e:
                logger.debug(f"Skipping row due to parsing error: {e}")
                continue
                
        return failures

    def verify_resilience(self, consecutive_successes: int) -> bool:
        """
        Validates if a rule has reached a resilience threshold.
        """
        return consecutive_successes >= 100

if __name__ == "__main__":
    sce = ARASceptic()
    examples = sce.find_counter_examples(root_target=2, limit=5)
    print(f"Counter Examples Found: {len(examples)}")
