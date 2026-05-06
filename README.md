# Math Prediction Service

A production-ready machine learning service for mathematical predictions and forensic analysis.

---

## 🚀 Features

- **FastAPI-based REST API**: High-performance asynchronous API for model serving.
- **Sovereign AI Decision Engine**: A hybrid forensic engine using GUR (Grand Unified Rule), Swarm Consensus, and Hyper-Recursion.
- **Multi-Engine Training Suite**: Advanced time-series forecasting via **Prophet**, **Amazon Chronos**, **NeuralForecast (N-HiTS)**, and **XGBoost**.
- **Experiment Tracking**: Integrated with **MLflow** for rigorous tracking of parameters, metrics, and artifacts.
- **Model Versioning & Registry**: Built-in system for registering, versioning, and loading models.
- **Forensic Auditing**: Recursive backtracking and temporal DNA analysis to ensure 100% causal consistency.
- **Dockerized Deployment**: Fully containerized with Docker and Docker Compose for easy orchestration.
- **Comprehensive Test Suite**: Unit and integration tests using Pytest.
- **Type-hinted & Documented**: Clean, maintainable code following modern Python best practices.

---

## 🛠 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/abin54/math_prediction.git
cd math_prediction
```

### 2. Install Dependencies

Using the provided Makefile for standard installation:

```bash
make install
```

### 3. Train the Sovereign Engine

Run the multi-engine training pipeline to calibrate Prophet, Chronos, and NeuralForecast models:

```bash
python train.py
```

### 4. Analyze Today's Singularity

Execute the Sovereign Judge Master to generate today's forensic prediction:

```bash
python Sovereign_Judge_Master.py
```

### 5. Start the API

Launch the FastAPI development server:

```bash
uvicorn src.api.main:app --reload
```

---

## 📖 API Documentation

Once the API is running, you can access the interactive documentation:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ⚙️ Configuration

All system parameters, including model hyperparameters, feature schemas, and API settings, are managed in the `configs/` directory.

- **Base Config**: `configs/base.yaml`
- **Production Config**: `configs/production.yaml`

---

## 🐳 Docker Deployment

To spin up the entire stack (API + Redis) using Docker:

```bash
make docker-build
make docker-up
```

---

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.
