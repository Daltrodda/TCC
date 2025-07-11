from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

app = FastAPI()
requests_total = Counter('requests_total', 'Total number of requests', ['endpoint'])

@app.get("/health")
def health():
    return {"status": "users service ok"}

@app.get("/users")
def list_users():
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
