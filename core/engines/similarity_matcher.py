import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Any
from core.utils.forensic_logger import ForensicLogger

class SimilarityMatcher:
    """
    Implements similarity-based historical context building for numerical sequences.
    Based on the 'Next-Number-Prediction' pattern (Similarity Search via Relative Differences).
    """

    def __init__(self, logger=None):
        self.logger = logger if logger else ForensicLogger()

    @staticmethod
    def mse(a: np.ndarray, b: np.ndarray) -> float:
        """Calculate the Mean Squared Error between two arrays."""
        return np.mean((a - b) ** 2)

    @staticmethod
    def relative_differences(arr: np.ndarray) -> np.ndarray:
        """Calculate relative differences between consecutive elements."""
        arr = np.array(arr, dtype=float)
        # Handle zero division by adding a tiny epsilon
        return np.diff(arr) / (arr[:-1] + 1e-9)

    def similarity_search(self, query: List[float], historical_data: pd.DataFrame, 
                          target_col: str = 'Open', n: int = 5) -> List[Dict[str, Any]]:
        """
        Search for the top N most similar sequences in the historical data.
        """
        self.logger.info(f"Searching for Top {n} Historical Twin Nodes ({target_col})...")
        query_arr = np.array(query)
        query_diffs = self.relative_differences(query_arr)
        
        # We need at least one more element in history than in query_diffs
        history_vals = historical_data[target_col].values
        seq_size = len(query_arr)
        
        matches = []
        
        # Iterate through history using a sliding window
        for i in range(len(history_vals) - seq_size - 1):
            window = history_vals[i:i+seq_size]
            target_result = history_vals[i+seq_size] # The value that followed this sequence
            
            try:
                window_diffs = self.relative_differences(window)
                error = self.mse(query_diffs, window_diffs)
                
                matches.append({
                    'index': i,
                    'date': historical_data.iloc[i+seq_size]['Date'],
                    'sequence': window,
                    'result': target_result,
                    'error': error
                })
            except Exception:
                continue
                
        # Sort by error (ascending)
        matches.sort(key=lambda x: x['error'])
        return matches[:n]

    def format_for_ollama(self, matches: List[Dict[str, Any]]) -> str:
        """Format the 'Twin Nodes' for Socratic Audit context."""
        context = "  [Similarity Audit] Identified Twin Nodes in 1972-2026 Dataset:\n"
        for i, match in enumerate(matches, 1):
            context += f"    Node {i}: Date {match['date']} | Seq {list(match['sequence'])} -> Result {match['result']} (MSE: {match['error']:.6f})\n"
        
        self.logger.info(f"Identified {len(matches)} Twin Nodes for Socratic Audit.")
        return context

if __name__ == "__main__":
    # Internal test
    print("  [Test] Initializing Similarity Matcher...")
    matcher = SimilarityMatcher()
    
    # Synthetic test data
    history = pd.DataFrame({
        'Date': ['1990-01-01', '1990-01-02', '1990-01-03', '1990-01-04', '1990-01-05', '1990-01-06'],
        'Open': [1, 2, 3, 4, 3, 2]
    })
    
    query = [1, 2, 3]
    results = matcher.similarity_search(query, history, 'Open', 2)
    print(matcher.format_for_ollama(results))
