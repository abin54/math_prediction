from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import time
from typing import List, Dict, Any
from src.inference.predictor import MathPredictor
from src.utils.config import get_config
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

app = FastAPI(
    title="Sovereign AI Math Prediction API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
config = get_config()
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Rate Limiter (For Production Readiness demo)
REQUEST_COUNT = 0
MAX_REQUESTS = 100

@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    global REQUEST_COUNT
    REQUEST_COUNT += 1
    if REQUEST_COUNT > MAX_REQUESTS:
        return JSONResponse(status_code=429, content={"detail": "Too many requests"})
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Sovereign AI Math Prediction API",
        "docs": "/docs",
        "health": "/health",
        "metrics": "/metrics"
    }

@app.get("/metrics")
async def get_metrics():
    return {
        "total_requests": REQUEST_COUNT,
        "uptime": "stable",
        "active_model": config.model.type
    }

# Dependency to get predictor
def get_predictor():
    config = get_config()
    return MathPredictor(model_path=config.model.path)

class PredictionRequest(BaseModel):
    features: List[float]
    
class PredictionResponse(BaseModel):
    prediction: float
    confidence: float
    model_version: str
    latency_ms: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest, predictor: MathPredictor = Depends(get_predictor)):
    try:
        start_time = time.perf_counter()
        result = predictor.predict(request.features)
        latency = (time.perf_counter() - start_time) * 1000
        
        return PredictionResponse(
            prediction=result.value,
            confidence=result.confidence,
            model_version="v1.0.0",
            latency_ms=round(latency, 2)
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": True}

@app.get("/model/info")
async def model_info(predictor: MathPredictor = Depends(get_predictor)):
    return {
        "model_path": str(predictor.model_path),
        "n_features": predictor.n_features
    }
