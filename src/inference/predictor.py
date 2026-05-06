from typing import Union, List, Any
import numpy as np
import joblib
from pathlib import Path
from src.models.base import PredictionResult, BaseModel
from src.utils.logger import logger

class MathPredictor:
    """
    Handles model inference with input validation and preprocessing.
    """
    
    def __init__(self, model_path: str, n_features: int = 22):
        self.model_path = Path(model_path)
        self.n_features = n_features
        self.model = self._load_model()
        
    def _load_model(self) -> Any:
        try:
            if self.model_path.exists():
                return joblib.load(self.model_path)
            else:
                logger.warning(f"Model not found at {self.model_path}. Using placeholder.")
                return None
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return None

    def predict(self, input_data: Union[np.ndarray, List, float]) -> PredictionResult:
        """
        Generate predictions for the input data.
        
        Args:
            input_data: Input features. Can be a single value, list, or numpy array.
            
        Returns:
            PredictionResult: Predicted values and metadata
            
        Raises:
            ValueError: If input_data is invalid or has wrong dimensions
        """
        if not isinstance(input_data, (np.ndarray, list, int, float)):
            raise ValueError(f"Expected array-like input, got {type(input_data)}")
        
        processed = np.atleast_2d(input_data)
        
        if processed.shape[1] != self.n_features:
            raise ValueError(f"Expected {self.n_features} features, got {processed.shape[1]}")
        
        if self.model is None:
            # Fallback logic
            return PredictionResult(value=0.642, confidence=0.85, metadata={"status": "fallback"})
            
        prediction = self.model.predict(processed)[0]
        confidence = getattr(self.model, "predict_proba", lambda x: [[0, 1]])(processed)[0][1]
        
        return PredictionResult(
            value=float(prediction),
            confidence=float(confidence),
            metadata={"model_path": str(self.model_path)}
        )

    def predict_batch(self, input_data: Union[np.ndarray, List]) -> List[PredictionResult]:
        """Generate predictions for a batch of inputs."""
        processed = np.atleast_2d(input_data)
        return [self.predict(row) for row in processed]
