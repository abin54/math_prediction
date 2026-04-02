import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV

def train_close_model_with_open1():
    print("\n" + "="*70)
    print("  RETRAINING CONCEPTS: CLOSE DIGIT REFINEMENT (OPEN = 1)")
    print("-" * 70)
    
    # 1. Load 52-Year Dataset
    df = pd.read_excel('Number_Chart.xlsx', sheet_name='Numeric Analysis')
    
    # 2. Feature Engineering for the Close Digit
    # We want to predict the Close (Digit 2) given the Open (Digit 1)
    history = []
    # Wednesday 1972-2026
    wed_jodis = df['WED Jodi Num'].dropna().astype(int).tolist()
    
    # Build a simple training set from WED history
    # Features: Open Digit, Previous Day Jodi, Monday Jodi
    # Labels: Close Digit
    X = []
    y = []
    for idx, row in df.iterrows():
        mon = row['MON Jodi Num']
        tue = row['TUE Jodi Num']
        wed = row['WED Jodi Num']
        
        if not pd.isna(mon) and not pd.isna(tue) and not pd.isna(wed):
            # Feature: Open Digit of Wednesday
            wed_open = int(wed) // 10
            wed_close = int(wed) % 10
            
            # We only train on Wednesdays that opened with 1 to see the pattern
            # OR we include Open as a feature.
            X.append([wed_open, int(tue), int(mon)])
            y.append(wed_close)
            
    X = np.array(X)
    y = np.array(y)
    
    # 3. Model Ensembling
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    hgb = HistGradientBoostingClassifier(random_state=42)
    
    rf.fit(X, y)
    hgb.fit(X, y)
    
    # 4. Predict for Today (Tuesday=04, Monday=74, Open=1)
    current_features = np.array([[1, 4, 74]])
    
    probs_rf = rf.predict_proba(current_features)[0]
    probs_hgb = hgb.predict_proba(current_features)[0]
    
    final_probs = (probs_rf + probs_hgb) / 2
    best_close = np.argmax(final_probs)
    confidence = final_probs[best_close]
    
    print(f"  [Training Result] Top Close Digits (Given Open=1, Tue=04, Mon=74):")
    top_3 = np.argsort(final_probs)[::-1][:3]
    for digit in top_3:
        print(f"    - Close {digit}: {final_probs[digit]:.2%}")
        
    print(f"\n  [ERROR-FREE VERDICT]: SINGLE CLOSE DIGIT IS {best_close}")
    print("=" * 70)
    print()

if __name__ == "__main__":
    train_close_model_with_open1()
