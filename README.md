# Math Prediction API

A production-ready REST API for forecasting daily numerical sequences using 52 years of historical data.

---

## 🚀 Architecture

- **Model**: XGBoost Regressor optimized for **Mean Absolute Error (MAE)**.
- **Features**: Cyclical time encoding (Fourier terms), recursive lag features (1, 7, 30, 365 days), and rolling volatility statistics.
- **API**: FastAPI with automatic OpenAPI (Swagger) documentation.
- **Persistence**: SQLAlchemy + SQLite for historical update retention.
- **Deployment**: Fully Dockerized for environment parity.

---

## 🔍 Why This Works

Standard regression fails on time-series because it ignores temporal dependencies. This service engineers **Temporal Features** (e.g., capturing weekly seasonality via sine/cosine transforms and 365-day lags) to allow tree-based models to understand chronological patterns without data leakage.

The system utilizes a **Recursive Forecasting** strategy for multi-day horizons, ensuring that future projections are grounded in the model's own predicted state.

---

## 🛠 Endpoints

- `GET /forecast/next7`: Returns a high-fidelity 7-day forecast.
- `POST /update`: Ingests daily actual data into the SQLite persistence layer to prevent concept drift.
- `GET /health`: System liveness and model status check.

---

## 📦 Quick Start

### 1. Build & Run
```bash
docker build -t math-forecast .
docker run -p 8000:8000 math-forecast
```

### 2. Manual Training
```bash
python train_production.py
```

### 3. Automated Retraining
The system includes a **GitHub Actions** workflow (`retrain.yml`) that automatically recalibrates the model on the 1st of every month using the latest ground-truth data.

---

## ⚖️ License
Distributed under the MIT License. See `LICENSE` for more information.
