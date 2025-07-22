from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, wait_for_db
from app.models import Base
from app.routes import auth

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:5173"],  # ou ["*"] para testes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas de autenticação
app.include_router(auth.router, prefix="/auth")

# Cria as tabelas no banco automaticamente
@app.on_event("startup")
async def startup():
    await wait_for_db()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Apenas executado se for chamado diretamente
if __name__ == "__main__":
    import uvicorn
    import ssl
    import os

    base_path = os.path.dirname(__file__)
    cert_path = os.path.join(base_path, "../cert/cert.pem")
    key_path = os.path.join(base_path, "../cert/key.pem")

    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=cert_path, keyfile=key_path)

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        ssl_certfile=cert_path,
        ssl_keyfile=key_path
    )
