from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

app = FastAPI()
requests_total = Counter('requests_total', 'Total number of requests', ['endpoint'])

@app.get("/health")
def health():
    return {"status": "auth service ok"}

@app.post("/login")
def login():
    # Simulação de login
    return {"token": "fake-jwt-token"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

@app.post("/token")
def create_token():
    expire = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode({"exp": expire}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}
