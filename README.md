# MiroFish Matka Prediction Engine

An advanced, multi-agent swarm intelligence system for predicting Jodi numbers using a combination of historical statistics, machine learning, and LLM reasoning.

## 🚀 Key Features

*   **Multi-Agent Swarm**: 6 specialized agents (Stat, Trend, Transition, Cycle, ML, LLM) voting in an ensemble.
*   **GPU Accelerated**: Utilizes **XGBoost** with CUDA on an NVIDIA GTX 1650 for high-fidelity pattern recognition.
*   **Local LLM Reasoning**: Integrated with **Ollama (llama3.2:3b)** to provide human-like context and reasoning.
*   **Automated Background Fetcher**: Internet-connected results scraper (`auto_updater.py`) to keep datasets fresh in real-time.
*   **Safe Resource Management**: Optimized for 8GB RAM systems with strict memory limiting.

## 🛠️ Components

1.  **`predict_today.py`**: The main entry point for daily forecasts.
2.  **`swarm_predictor.py`**: The core ensemble engine.
3.  **`auto_updater.py`**: The background results monitor.
4.  **`train_small_model.py`**: High-performance feature extractor and model trainer.

## 📖 Usage

### 1. Daily Prediction
To generate the latest Top-4 Jodi forecast:
```bash
python predict_today.py
```

### 2. Background Updates
Keep your dataset updated automatically:
```bash
# Run the background fetcher
python auto_updater.py
```
*(Or use `start_updater.bat` on Windows)*

## 📊 Technical Stack
- **Languages**: Python 3.13+
- **ML**: XGBoost (with CUDA), Scikit-Learn
- **Data**: Pandas, OpenPyxl
- **LLM**: Ollama (Local)
- **Infrastructure**: GitHub CLI, BeautifulSoup4

---
**Disclaimer**: This project is for educational and statistical analysis purposes only. Matka is a game of chance and this tool provides no guarantees of success.
