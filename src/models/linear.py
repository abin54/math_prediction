from src.models.base import BaseModel, PredictionResult
from sklearn.linear_model import LinearRegression
import joblib
import numpy as np

class LinearRegressionModel(BaseModel):
    def __init__(self, **kwargs):
        self.model = LinearRegression(**kwargs)
        
    def train(self, X: np.ndarray, y: np.ndarray, **kwargs) -> None:
        self.model.fit(X, y)
        
    def predict(self, X: np.ndarray) -> PredictionResult:
        val = self.model.predict(X)[0]
        return PredictionResult(value=float(val), confidence=1.0)
        
    def save(self, path: str) -> None:
        joblib.dump(self.model, path)
        
    def load(self, path: str) -> None:
        self.model = joblib.load(path)
