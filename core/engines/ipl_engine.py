import numpy as np
from typing import Tuple, Optional
from core.utils.logger import sovereign_logger as logger
from core.utils.config_manager import ConfigManager
from core.utils.path_manager import PathManager
from core.models.match_state import MatchState

# We'll assume the hybrid_model is moved to core/models/ or kept in ipl_engine
# For now, let's keep the import but make it cleaner
try:
    from ipl_engine.hybrid_model import HybridEnsemble
except ImportError:
    logger.warning("HybridEnsemble not found in ipl_engine. Using placeholder logic.")
    class HybridEnsemble:
        def load_models(self, path): pass
        def predict(self, static, seq): return 0.642

class IPLEngine:
    """
    Core engine for IPL win probability and momentum analysis.
    """
    
    def __init__(self):
        self.model_path = str(PathManager.MODELS / "hybrid_ensemble")
        self.ensemble = HybridEnsemble()
        self._initialize_model()
        
    def _initialize_model(self):
        """Loads model weights if available."""
        try:
            if PathManager.get_model_path("hybrid_ensemble_xgb.json").exists():
                self.ensemble.load_models(self.model_path)
                logger.info(f"Hybrid Logic Nodes initialized from {self.model_path}")
            else:
                logger.warning(f"Model weights not found at {self.model_path}. Using synthetic heuristics.")
        except Exception as e:
            logger.error(f"Failed to load models: {e}. Falling back to heuristics.")

    def predict_win_probability(self, state: MatchState, batting_team: str = "MI") -> float:
        """
        Calculates the win probability for the batting team.
        """
        logger.info(f"Predicting win probability for {batting_team}")
        
        # In a production scenario, we'd map MatchState to the model's feature vector
        # Placeholder static/seq features
        static_feats = np.zeros((1, 22)) 
        seq_feats = np.zeros((1, 18, 3))
        
        try:
            win_prob = self.ensemble.predict(static_feats, seq_feats)
        except Exception as e:
            logger.warning(f"Inference failed: {e}. Using fallback.")
            win_prob = 0.642 
            
        return float(win_prob)

    def stream_analysis(self, current_score: str, current_overs: float) -> Tuple[float, float]:
        """
        Specialized inference for live streaming data (ball-by-ball).
        """
        logger.debug(f"Streaming analysis for score {current_score} at {current_overs} overs")
        
        try:
            runs, wickets = map(int, current_score.split('/'))
        except ValueError:
            logger.error(f"Invalid score format: {current_score}")
            return 0.0, 0.0
            
        crr = runs / current_overs if current_overs > 0 else 0
        
        # Next 6-ball projection logic (refactored)
        next_rr = max(4.0, crr * 1.1) if wickets < 3 else crr * 0.9
        wicket_prob = 0.15 + (wickets * 0.05) + (crr * 0.02)
        
        return float(next_rr), float(wicket_prob)
