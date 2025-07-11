from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response
from pydantic import BaseModel

app = FastAPI()
requests_total = Counter('requests_total', 'Total number of requests', ['endpoint'])

class PredictRequest(BaseModel):
    feature1: float
    feature2: float

@app.get("/health")
def health():
    return {"status": "ml service ok"}

@app.post("/predict")
def predict(req: PredictRequest):
    # Lógica de predição fake
    result = 1 if req.feature1 + req.feature2 > 1 else 0
    return {"prediction": result}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
