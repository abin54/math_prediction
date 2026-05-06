import pandas as pd
import numpy as np
import pytest
from src.features import FeatureEngineer

def test_build_features_shape():
    # Create dummy data (must be > 365 days for lag_365)
    dates = pd.date_range(start='2020-01-01', periods=400)
    values = np.random.randn(400)
    df = pd.DataFrame({'ds': dates, 'value': values})
    
    df_fe = FeatureEngineer.build_features(df)
    
    # Check that output is not empty
    assert not df_fe.empty
    
    # Check that all expected columns are present
    expected_cols = FeatureEngineer.get_feature_columns()
    for col in expected_cols:
        assert col in df_fe.columns

def test_feature_columns_consistency():
    cols = FeatureEngineer.get_feature_columns()
    assert len(cols) == 14
    assert 'lag_365' in cols
