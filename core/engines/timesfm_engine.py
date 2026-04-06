import os
import sys
import numpy as np
import torch
from typing import List, Optional
from core.utils.forensic_logger import ForensicLogger

# Add ipl_engine to path so 'import timesfm' works (where ipl_engine/timesfm/ is the package)
sys.path.append(os.path.join(os.getcwd(), 'ipl_engine'))

try:
    # We must import from the local source
    # The structure is ipl_engine/timesfm/timesfm_2p5/timesfm_2p5_torch.py
    from timesfm.timesfm_2p5.timesfm_2p5_torch import TimesFM_2p5_200M_torch
    from timesfm import configs
except ImportError as e:
    print(f"  [Error] Failed to import TimesFM from local source: {e}")
    # Fallback to dummy if needed
    TimesFM_2p5_200M_torch = None

class TimesFMEngine:
    """
    Foundational Forecasting Engine using Google's TimesFM-2.5-200M.
    Handles zero-shot time-series forecasting for numerical sequences.
    """
    
    def __init__(self, logger=None, model_dir: str = "models/timesfm"):
        self.logger = logger if logger else ForensicLogger()
        self.model_dir = model_dir
        self.model = None
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        
        if TimesFM_2p5_200M_torch:
            self._load_foundation_model()

    def _load_foundation_model(self):
        self.logger.info(f"Loading TimesFM Foundation Model from {self.model_dir}...")
        try:
            # Note: TimesFM_2p5_200M_torch uses Safetensors via PyTorchModelHubMixin
            # Since we downloaded manually to models/timesfm, we pass it as model_id
            self.model = TimesFM_2p5_200M_torch.from_pretrained(
                self.model_dir,
                local_files_only=True,
                torch_compile=False # Disable compile for Windows compatibility
            )
            
            # Set up default forecast config
            self.model.compile(
                configs.ForecastConfig(
                    max_context=512,
                    max_horizon=32,
                    normalize_inputs=True,
                    use_continuous_quantile_head=True,
                    force_flip_invariance=True,
                    infer_is_positive=True,
                    fix_quantile_crossing=True,
                )
            )
            self.logger.info("Foundation Consensus: TimesFM-2.5 Nodes active.")
        except Exception as e:
            self.logger.warning(f"TimesFM Load Failure: {e}. Foundational forecast disabled.")
            self.model = None

    def forecast(self, sequence: List[float], horizon: int = 1) -> Optional[np.ndarray]:
        """
        Predict the next N values in the sequence.
        
        Args:
            sequence: Historical numerical sequence.
            horizon: Number of steps to forecast.
        """
        if not self.model:
            return None
            
        try:
            # Inputs: list of numpy arrays
            inputs = [np.array(sequence, dtype=np.float32)]
            
            point_forecast, _ = self.model.forecast(
                horizon=horizon,
                inputs=inputs
            )
            
            # Return the first forecast array
            return point_forecast[0]
        except Exception as e:
            self.logger.error(f"Foundation Forecast Error: {e}")
            return None

if __name__ == "__main__":
    # Internal test
    print("  [Test] Initializing TimesFM Engine...")
    engine = TimesFMEngine()
    
    if engine.model:
        # Synthetic sequence: 1, 2, 3, 4, 5...
        test_seq = [float(i) for i in range(1, 11)]
        res = engine.forecast(test_seq, horizon=1)
        if res is not None:
            print(f"    - Input: {test_seq}")
            print(f"    - Foundation Forecast: {res}")
    else:
        print("    - Foundation model not available.")
