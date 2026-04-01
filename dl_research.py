import pandas as pd
import numpy as np
import os

def get_hurst_exponent(ts):
    """Simple R/S version for Hurst Exponent."""
    lags = range(2, 20)
    tau = [np.sqrt(np.std(np.subtract(ts[lag:], ts[:-lag]))) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0] * 2.0

def run_dl_research():
    file = "Number_Chart.xlsx"
    if not os.path.exists(file):
        print("File not found.")
        return
        
    df = pd.read_excel(file, sheet_name="Numeric Analysis")
    sequence = []
    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
    for idx, row in df.iterrows():
        for d in days:
            v = row[f"{d} Jodi Num"]
            if not pd.isna(v): sequence.append(float(v))
    
    seq = np.array(sequence)
    
    # 1. Hurst Exponent (Long-term persistence)
    h = get_hurst_exponent(seq)
    print("\n" + "="*70)
    print(f"  DL RESEARCH: HURST EXPONENT = {h:.4f}")
    if h > 0.55:
        print("    RESULT: PERSISTENT TREND (Ideal for LSTM/RNN).")
    elif h < 0.45:
        print("    RESULT: MEAN-REVERTING (Ideal for CNN/TCN).")
    else:
        print("    RESULT: RANDOM WALK (Hard to predict with DL).")
    
    # 2. FFT (Identification of Primary Periodicities)
    seq_detrended = seq - np.mean(seq)
    fft_vals = np.abs(np.fft.fft(seq_detrended))
    freqs = np.fft.fftfreq(len(seq))
    indices = np.where(freqs > 0)[0]
    top_indices = indices[np.argsort(fft_vals[indices])[-3:][::-1]]
    
    print("\n  DL RESEARCH: DOMINANT CYCLES (Top 3 FFT peaks)")
    for idx in top_indices:
        period = 1 / freqs[idx]
        print(f"    Cycle: {period:.2f} days")

    print("\n" + "="*70)

if __name__ == "__main__":
    run_dl_research()
