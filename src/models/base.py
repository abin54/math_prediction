from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional
import numpy as np

@dataclass
class PredictionResult:
    value: float
    confidence: float
    metadata: Dict[str, Any] = None

class BaseModel(ABC):
    """
    Abstract base class for all machine learning models.
    """
    
    @abstractmethod
    def train(self, X: np.ndarray, y: np.ndarray, **kwargs) -> None:
        pass
    
    @abstractmethod
    def predict(self, X: np.ndarray) -> PredictionResult:
        pass
    
    @abstractmethod
    def save(self, path: str) -> None:
        pass
    
    @abstractmethod
    def load(self, path: str) -> None:
        pass
