import xgboost as xgb
print("XGBoost version:", xgb.__version__)
d = xgb.DMatrix([[1,2,3]])
try:
    bst = xgb.train({'tree_method':'hist', 'device':'cuda:0'}, d, 1)
    print("GPU (device=cuda:0): OK")
except Exception as e:
    print(f"GPU failed: {e}")
    print("Will use CPU fallback")
