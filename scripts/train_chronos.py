import torch
import numpy as np
import pandas as pd
from chronos import ChronosPipeline
import os

# Load the prepared data
context = np.load('data/processed/chronos_data.npy')

print("--- [CHRONOS INFERENCE] ---")
# Load the pre-trained model
pipeline = ChronosPipeline.from_pretrained(
    "amazon/chronos-t5-small",
    device_map="cpu", # Use CPU as requested
    torch_dtype=torch.bfloat16,
)

# Predict the next 30 days
# We pass the last 1000 days as context to avoid overwhelming the model
prediction = pipeline.predict(torch.tensor(context[-1000:]), prediction_length=30)

# Take the mean for the actual number
predicted_numbers = prediction.mean(dim=0).numpy()
print(f"Chronos Prediction for tomorrow: {predicted_numbers[0][0]:.2f}")

# Save results
os.makedirs("models/forecasts", exist_ok=True)
np.save("models/forecasts/chronos_prediction.npy", predicted_numbers)
print("Chronos predictions saved to models/forecasts/chronos_prediction.npy")
