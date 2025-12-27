## ==============================================================
## 0. Import neccessary libraries
## ==============================================================
import os
import logging
import joblib
import numpy as np
import pandas as pd
from io import StringIO

from datetime import datetime
from contextlib import asynccontextmanager
from typing import List

from pydantic import BaseModel, Field

from fastapi import (
  FastAPI, 
  Depends, 
  File, 
  UploadFile, 
  HTTPException, 
  BackgroundTasks,
  Request
)


from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader


## ==============================================================
## 1. Logging setup
## ==============================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("iris-api")


## ==============================================================
## 2. Security - API key
## ==============================================================

API_KEY = "api-key-2025"
api_key_header = APIKeyHeader(name="API-key")

def require_api_key(api_key: str = Depends(api_key_header)):
  if api_key != API_KEY:
    raise HTTPException(status_code=403, detail="Invalid API key")
  return api_key

## ==============================================================
## 3. Dependency injection: Model artifacts
## ==============================================================
class IrisModel:
  def __init__(self):
    base_dir = os.path.dirname(__file__)
    artifacts_dir = os.path.join(base_dir, "artifacts")
    self.model = joblib.load("artifacts/model.pkl")
    self.feature_names = joblib.load("artifacts/feature_names.pkl")
    self.class_names = joblib.load("artifacts/class_names.pkl")
    logger.info("artifacts are loaded successfully")


## ==============================================================
## 4. Create the lifespan method
## ==============================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
  app.state.model = IrisModel()
  logger.info("Service started - model ready!")

  yield 

  app.state.model = None
  logger.info("Service shutdown")


## ==============================================================
## 5. create the FastAPU
## ==============================================================

app = FastAPI(
  title="Iris Prediction Service",
  description="Secure batch classification fo iris species",
  lifespan=lifespan
)

## ==============================================================
## 6. Middleware: CORS + request logging
## ==============================================================

app.add_middleware(
  CORSMiddleware, 
  allow_origins=["https://iris-prediction-frontend.example.com"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)



class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = datetime.utcnow()
        response = await call_next(request)
        duration = (datetime.utcnow() - start_time).total_seconds()
        logger.info(
            f"{request.client.host if request.client else 'unknown'} | "
            f"{request.method} {request.url.path} | "
            f"{response.status_code} | {duration:.3f}s"
        )
        return response
  
app.add_middleware(RequestLoggingMiddleware)

## ==============================================================
## 7. Pydantic Models 
## ==============================================================
class PredictResult(BaseModel):
  predicted_species: str
  probabilities: dict[str, float]

class BatchResponse(BaseModel):
  total_processed: int
  predictions: List[PredictResult]
  timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


## ==============================================================
## 8. Dependency (get models)
## ==============================================================

def get_iris_model():
  if app.state.model is None:
    raise HTTPException(503, "Model not ready")
  return app.state.model


## ==============================================================
## 9. Background task (log upload)
## ==============================================================

def log_upload_summary(filename: str, row_count: int, researcher_ip: str):
  logger.info(f"UPLOAD | {filename} | {row_count} rows | from {researcher_ip}")



## ==============================================================
## 10. Main endpoint (File upload + Batch Prediction)
## ==============================================================
@app.post("/batch-predict-csv", response_model=BatchResponse)
async def batch_predict_csv(
    file: UploadFile = File(...),                     # ← ONLY default argument → must be first
    background_tasks: BackgroundTasks,
    model=Depends(get_iris_model),
    api_key: str = Depends(require_api_key),
    request: Request,
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, detail="Only CSV files allowed")

    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode("utf-8")))

    if list(df.columns) != model.feature_names:
        raise HTTPException(400, f"Expected columns: {model.feature_names}")

    input_data = df.values
    preds = model.model.predict(input_data)
    probas = model.model.predict_proba(input_data)

    results = []
    for pred_class, proba in zip(preds, probas):
        probabilities = {s: float(p) for s, p in zip(model.class_names, proba)}
        results.append(PredictResult(
            predicted_species=model.class_names[pred_class],
            probabilities=probabilities
        ))

    # Fix the NameError: define client_ip here
    client_ip = request.client.host if request.client else "unknown"

    # Now safe to use
    background_tasks.add_task(log_upload_summary, file.filename, len(df), client_ip)

    return BatchResponse(
        total_processed=len(df),
        predictions=results
    )