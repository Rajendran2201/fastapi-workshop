## ===========================================================================
## 0. Import the necessary libraries 
## ===========================================================================

from fastapi import FastAPI, HTTPException

# for defining and validating input/output data
from pydantic import BaseModel, Field

# for batch prediction
from typing import List

import pandas as pd
import numpy as np
import joblib

# for startup/shutdown logic 
from contextlib import asynccontextmanager    


## ===========================================================================
## 1. Initialise the global variables as None
## ===========================================================================

# initialise globals 
model = None
feature_names = None
class_names = None


## ===========================================================================
## 2. Load the artifacts and clean up them after usage
## ===========================================================================

# load the model and metadata 
@asynccontextmanager
async def load_artifacts(app: FastAPI):     # runs once the server starts
  global model, feature_names, class_names

  # load the artifacts
  model = joblib.load("artifacts/model.pkl")
  feature_names = joblib.load("artifacts/feature_names.pkl")
  class_names = joblib.load("artifacts/class_names.pkl")
  print("model loaded successfully")


  yield   # application runs here


# release resources after usage - cleans up memory
  print("cleaning up on shutdown")
  model = None
  feature_names = None
  class_names = None
  print("cleanup complete")

## ===========================================================================
## 3. Create the FastAPI()
## ===========================================================================


# create the fastapi 
# sets the metadata in docs 
# it uses the load_artifacts function for startup/shutdown
app = FastAPI(
  title="Iris Species Classifier", 
  version="1.0", 
  lifespan=load_artifacts
)


## ===========================================================================
## 4. Create an Input Model
## ===========================================================================


# request model 
# ... : required paramater
# ge=0 : ensures that all values are greater than or equal to 0 
# examples helps to generate nice docs 

class IrisFeatures(BaseModel):
  sepal_length: float = Field(..., ge=0, description="Sepal length in cm")
  sepal_width: float = Field(..., ge=0, description="Sepal width in cm")
  petal_length: float = Field(..., ge=0, description="Petal length in cm")
  petal_width: float = Field(..., ge=0, description="Petal width in cm")

  model_config = {
    "json_schema_extra":{
      "examples": [
        {
          "sepal_length": 5.1,
          "sepal_width": 3.5, 
          "petal_length": 1.4, 
          "petal_width": 0.2
        }
      ]
    }
  }

## ===========================================================================
## 5. Create an Output Model
## ===========================================================================

# response model 
class PredictionResponse(BaseModel):
  predicted_class: int
  predicted_species: str
  probabilities: dict[str, float]
  model_version: str="1.0.0"


## ===========================================================================
## 6. Create a method for Health Check
## ===========================================================================

# health check 
@app.get("/health")
def health():
  return {"status": "healthy"}


## ===========================================================================
## 7. Create a method for Model Metadata
## ===========================================================================

# get model info/meta data
@app.get("/model/info")
def model_info():
  if feature_names is None or class_names is None:
    raise HTTPException(status_code=503, detail="Model not loaded yet")
  return {
    "features": feature_names, 
    "classes": class_names,
    "n_features": len(feature_names)
  }


## ===========================================================================
## 8. Write the method for prediction 
## ===========================================================================

# predict the output for the features 
@app.post("/predict", response_model=PredictionResponse)
def predict(features: IrisFeatures):
  if model is None:
    raise HTTPException(status_code=503, detail="model not loaded")
  try:
    input_data = np.array([[
      features.sepal_length,
      features.sepal_width, 
      features.petal_length, 
      features.petal_width
    ]])

    pred_class = int(model.predict(input_data)[0])
    pred_proba = model.predict_proba(input_data)[0]

    probabilities = {
      species : float(prob)
      for species, prob in zip(class_names, pred_proba)
    }

    return PredictionResponse(
      predicted_class=pred_class,
      predicted_species=class_names[pred_class],
      probabilities=probabilities
    )
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")
  

## ===========================================================================
## 9. Write the input model for batch prediction
## ===========================================================================

# Batch Prediction
class BatchIrisFeatures(BaseModel):
  instances: List[IrisFeatures] = Field(..., min_items=1, max_items=100)


## ===========================================================================
## 10. Write the method for batch prediction
## ===========================================================================


@app.post("/batch-predict", response_model=List[PredictionResponse])
def batch_predict(batch: BatchIrisFeatures):
  if model is None:
    raise HTTPException(status_code=503, detail="model not loaded")
  try: 
    input_data = np.array(
      [[
        item.sepal_length, 
        item.sepal_width, 
        item.petal_length, 
        item.petal_width
      ] for item in batch.instances]
    )

    preds = model.predict(input_data)
    probas = model.predict_proba(input_data)

    results = []
    for pred_class, proba in zip(preds, probas):
      probabilities = {
        species: float(p) for species, p in zip(class_names, proba)
      }
      results.append(PredictionResponse(
        predicted_class=int(pred_class),
        predicted_species=class_names[pred_class],
        probabilities=probabilities
      ))

    return results

  except Exception as e:
    raise HTTPException(status_code=500, detail=f'Batch inference error: {str(e)}')