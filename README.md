# 52-Year Daily Time Series Forecast

A production-ready REST API utilizing Direct Multi-Step XGBoost forecasting to predict daily numerical values based on 52 years of historical data.

---

## 🚀 Architecture

- **Models**: 7 independent XGBoost regressors (predicting Days 1 through 7 simultaneously to eliminate recursive compounding errors).
- **Features**: Temporal lags (1, 7, 30, 365 days), rolling statistics, and Fourier cyclical transformations.
- **Database**: SQLite (persisted via Docker volumes) to ingest actuals and prevent model drift.
- **API**: FastAPI.

---

## 🛠 Setup & Deployment

1.  Place your historical CSV (columns: date, value) in `data/raw_data.csv`.
2.  **Train models locally**: 
    ```bash
    docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/models:/app/models math-prediction python scripts/train.py
    ```
3.  **Start API**: 
    ```bash
    docker-compose up -d --build
    ```
4.  **View Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔗 Endpoints

- `GET /forecast/next7`: Retrieves 7-day forecast.
- `POST /update`: Ingests actual data for a given date.
- `GET /health`: Service healthcheck.

---

## ⚖️ License
Distributed under the MIT License.
