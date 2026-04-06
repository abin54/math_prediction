import pandas as pd
import os

class DataManager:
    """
    Unified Data Provider for the Sovereign Hub.
    Handles numeric conversion, holiday filtering, and high-performance retrieval.
    """
    
    def __init__(self, db_path="data/constitutional_master_v52.csv"):
        self.db_path = db_path
        self._data = None
        self.load_data()

    def load_data(self):
        """Load and sanitize the 52-year dataset."""
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"Master Database not found at {self.db_path}")
            
        self._data = pd.read_csv(self.db_path)
        self._data['Date'] = pd.to_datetime(self._data['Date'])
        
        # Globally handle non-numeric entries (Holidays, Errors)
        # We replace '*' and 'XX' with NaN so engines can skip them safely.
        for col in ['Open', 'Close']:
            if col in self._data.columns:
                self._data[col] = pd.to_numeric(self._data[col], errors='coerce')
        
        return self._data

    def get_data(self):
        """Returns the sanitized dataframe."""
        if self._data is None:
            self.load_data()
        return self._data

    def get_last_n_rows(self, n=10):
        """High-performance retrieval of recent history."""
        return self.get_data().tail(n)

    def get_friday_nodes(self):
        """Retrieves nodes specific to the Friday Loop."""
        df = self.get_data()
        return df[df['Date'].dt.day_name() == 'Friday'].dropna(subset=['Open'])

    def get_node_by_date(self, date_str):
        """Retrieves a specific historical node."""
        df = self.get_data()
        mask = df['Date'] == pd.to_datetime(date_str)
        return df[mask]
