from fastapi import FastAPI, Request, HTTPException
from jose import JWTError, jwt

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

app = FastAPI()

@app.middleware("http")
async def jwt_middleware(request: Request, call_next):
    # Permitir rotas públicas
    if request.url.path in ["/", "/public", "/login"]:
        return await call_next(request)

    # Verificar token JWT
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token não fornecido")
    token = auth.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user = payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    return await call_next(request)

@app.get("/")
def root():
    return {"message": "Gateway público"}

@app.get("/private")
def private_route(request: Request):
    return {"message": f"Olá, {request.state.user.get('nome')}", "perfil": request.state.user.get("perfil")}
