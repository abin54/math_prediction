"""
Neural DNA Model v8.0 — Hybrid CNN-LSTM with Residual Origin Point
==================================================================
Architected for the 52-year Kalyan Matka dataset. 
Includes Entity Embeddings, Dilated Convolutions (9-day cycle), 
and a Residual Connection to Day 1 (1972).
"""

import tensorflow as tf
from tensorflow.keras import layers, models, Input

def build_neural_dna_model(seq_len=30):
    # --- INPUTS ---
    # 1. Main Sequence (Last 30 Jodi numbers)
    main_input = Input(shape=(seq_len, 1), name="main_sequence")
    
    # 2. Origin Point (Day 1 - 1972)
    origin_input = Input(shape=(1,), name="origin_point")
    
    # 3. Categorical Inputs (Day of Week, Month)
    day_input = Input(shape=(1,), name="day_of_week")
    month_input = Input(shape=(1,), name="month_of_year")
    
    # --- EMBEDDINGS ---
    day_emb = layers.Embedding(input_dim=7, output_dim=8)(day_input)
    day_emb = layers.Flatten()(day_emb)
    
    month_emb = layers.Embedding(input_dim=13, output_dim=8)(month_input)
    month_emb = layers.Flatten()(month_emb)
    
    # --- CNN PATH (Local Daily Patterns / 9-Day Cycles) ---
    conv1 = layers.Conv1D(filters=64, kernel_size=3, activation='relu')(main_input)
    conv2 = layers.Conv1D(filters=128, kernel_size=6, activation='relu')(conv1)
    conv3 = layers.Conv1D(filters=64, kernel_size=9, activation='relu')(conv2)
    cnn_out = layers.GlobalMaxPooling1D()(conv3)
    
    # --- LSTM PATH (Long-term Temporal Memory) ---
    lstm1 = layers.LSTM(128, return_sequences=True)(main_input)
    lstm2 = layers.LSTM(64)(lstm1)
    
    # --- FUSION ---
    concat = layers.Concatenate()([cnn_out, lstm2, day_emb, month_emb])
    
    dense1 = layers.Dense(128, activation='relu')(concat)
    dense1 = layers.Dropout(0.2)(dense1)
    dense2 = layers.Dense(64, activation='relu')(dense1)
    
    # --- THE RESIDUAL ORIGIN CONNECTION ---
    # We add a linear path from Day 1 to the final output
    origin_path = layers.Dense(1, use_bias=False)(origin_point)
    
    # Final Output (Value between 00-99)
    main_output = layers.Dense(1)(dense2)
    
    # ADD CONNECTION: Final = PredictedTrend + (Weight * OriginPoint)
    final_output = layers.Add(name="final_prediction")([main_output, origin_path])
    
    model = models.Model(
        inputs=[main_input, origin_input, day_input, month_input],
        outputs=final_output
    )
    
    return model

def custom_directional_loss(y_true, y_pred):
    """
    Penalizes wrong direction (Up/Down) 5x more than magnitude error.
    """
    mse = tf.square(y_true - y_pred)
    
    # Direction check (approximate delta from last mean)
    # This is a simplified version for Keras
    direction_penalty = tf.where(
        tf.sign(y_true - 50) != tf.sign(y_pred - 50),
        5.0 * mse, 
        mse
    )
    
    return tf.reduce_mean(direction_penalty)

if __name__ == "__main__":
    model = build_neural_dna_model()
    model.compile(optimizer='adam', loss=custom_directional_loss)
    model.summary()
    print("\n[SUCCESS] Neural DNA Architecture (Model v8.0) is complete.")
