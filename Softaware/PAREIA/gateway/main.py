from fastapi import FastAPI
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

app = FastAPI()
requests_total = Counter('requests_total', 'Total number of requests', ['endpoint'])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "API Gateway"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

from fastapi import Request, HTTPException
from jose import jwt, JWTError

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

@app.middleware("http")
async def check_jwt(request: Request, call_next):
    if request.url.path.startswith("/metrics") or request.url.path == "/health":
        return await call_next(request)
    token = request.headers.get("Authorization")
    if token:
        try:
            jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
    else:
        raise HTTPException(status_code=401, detail="Authorization token missing")
    return await call_next(request)
