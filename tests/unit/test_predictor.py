import pytest
import numpy as np
from src.inference.predictor import MathPredictor

class TestMathPredictor:
    @pytest.fixture
    def predictor(self):
        # Initialize with dummy path, will use fallback
        return MathPredictor(model_path="non_existent_model.joblib", n_features=2)
    
    def test_predict_single(self, predictor):
        result = predictor.predict([1.0, 2.0])
        assert result.value == 0.642
    
    def test_predict_invalid_dimensions(self, predictor):
        with pytest.raises(ValueError, match="Expected 2 features"):
            predictor.predict([1.0])
    
    def test_predict_invalid_type(self, predictor):
        with pytest.raises(ValueError, match="Expected array-like"):
            predictor.predict("not valid")
