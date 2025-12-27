## What is FastAPI?

FastAPI is a modern, fast, web framework for building APIs with python based on 
- Starlette (web framework)
- Pydantic (data validation)

It is designed for type hints, automatic validation, and automatic API documentation. 

### Why is it used in ML systems?
From an ML engineering perspective, it solves key problems: 
- Input validation: `pydantic` models enforce schema correctness
- High throughput: supports `async` and `uvicorn`
- Rapid iteration: auto-reload during development
- Model serving: clean integration with pytorch and sklearn
- Documentation: auto-generated swagger UI

FastAPI is mainly used for model inference, feature services, LLM endpoints, and internal ML microservices. 

### A quick tour

Prerequisite: `pip install fastapi`

or 

`pip install "fastapi[standard]"`

```python
# example code - main.py

from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
  return {"Hey":"This is raj!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q : Union[str, None] = None):
  return {"item_id": item_id, "q":q}

```

Run the script using `fastapi dev main.py`

### Automatic API Documentation 

Open `http://127.0.0.1:8000/docs` to view the swagger UI

### Understanding the endpoints (GET, POST)

An endpoint is a combination of HTTP method and URL path that maps to a python function. 
Some of the most important HTTP methods are 
- GET
- POST
- PUT
- PATCH 
- DELETE


#### 1. GET - retrieve data (read)
- The GET endpoint is used to retrieve the data. 
- It must not modify the server state.
- It is mainly used for health checks, model metadata, and version info. 

```python 
@app.get("/health")       # HTTP method + Path
def health():
  return {"status" : "healthy"}
```

#### 2. POST - create a resource

- The POST endpoint i sused to send data for processing.
- It can modify the server state.
- It has a request body, usually JSON (validated with Pydantic).
- It can be used for prediction, uploading files, starting the training jobs.
- Each time the post method is called, a resource is created on the server. 


```python
@app.post("/predict")
def predict(features : dict):
  return {"prediction": 0.98}
```

#### 3. PUT - replace a resource (Updated entirely) 
- The PUT method is used to replace the entire reource at a specific URL with new data.

```python
from pydantic import BaseModel

class ModelUpdate(BaseModel):
  version: str
  path: str     # usually S3 path to new model file
  metadata: dict


@app.put("/models/{model_id}")
def replace_model(model_id: int, updated_model: ModelUpdate):
  # overwrite the entire model cofig
  models[model_id] = updated_model.dict()
  reload_model(model_id)
  return {"message" : f"Model {model_id} fully replaced with {updated_model.version}"}

```

#### 4. PATCH - partially updated a resource
- It is used when you want only specific fields of the resource to be updated. 
Eg: updating the model's metadata without replacing the while model

```python
from pydantic import BaseModel


class ModelPartialUpdate(BaseModel):
  description: str | None = None
  tags: list[str] | None = None
  accuracy: float | None = None

@app.patch("/models/{model_id}")
def partial_update(model_id: int, updated_data: ModelPartialUpdate):
  model = models.get(model_id)
  
  # check if the model exists 
  if not model:
      raise HTTPException(404, "Model not found")
  
  # update the provided fields
  data_to_update = updated_data.dict(exclude_unset=True)  # only sent fields are updated
  model.update(data_to_update)
  return model

```

#### 5. DELETE - remove a resource

- It helps to delete a resource 

```python

@app.delete("models/{model_id}")
def delete_model(model_id: int):
  if model_id not in models:
      raise HTTPException(404, "Model not found")
  
  del models[model_id]

  return {"message" : f"Model {model_id} deleted"}

```


