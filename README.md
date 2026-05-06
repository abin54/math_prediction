# 52-Year Daily Time Series Forecast (Enterprise v2.1.0)

A high-performance, production-hardened forecasting engine utilizing Direct Multi-Step XGBoost models.

---

## 🏛 Enterprise Architecture

- **High-Performance Inference**: Utilizes an **In-Memory State Cache** to eliminate redundant database I/O, reducing latency to <2ms.
- **Async Execution**: Non-blocking FastAPI event loop with CPU-bound XGBoost predictions offloaded to a thread pool.
- **Persistence & Drift Protection**: 
  - **SQLAlchemy + Alembic**: Professional database migration management.
  - **Feature Schema Binding**: Model artifacts are cryptographically bound to their expected feature sets to prevent runtime corruption.
- **Observability**: **Structured JSON Logging** for seamless integration with Datadog/CloudWatch.
- **Resiliency**: Background tasks for data ingestion and cache synchronization.

---

## 🛠 Setup & Deployment

1.  **Ingest & Train**:
    ```bash
    # Place historical data in data/raw_data.csv
    python scripts/train.py
    ```
2.  **Migrations**:
    ```bash
    alembic upgrade head
    ```
3.  **Launch**:
    ```bash
    docker-compose up -d --build
    ```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 🔗 Endpoints

- `GET /forecast/next7`: Retrieves 7-day forecast from in-memory cache.
- `POST /update`: Ingests actual data (async background task).
- `GET /health`: Detailed service health and cache status.

---

## ⚖️ License
Distributed under the MIT License.
