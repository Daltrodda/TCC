import asyncio
import time
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexão com o banco PostgreSQL usando asyncpg
DATABASE_URL = DATABASE_URL = "postgresql+asyncpg://auth_user:auth_pass@auth_db:5432/auth_db"

# Criação do engine assíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Habilita logs SQL no terminal
    future=True
)

# Session factory para sessões assíncronas
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base para os modelos
Base = declarative_base()

# Função para aguardar a conexão com o banco de dados estar pronta
async def wait_for_db():
    max_tries = 10
    for i in range(1, max_tries + 1):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ Banco de dados conectado com sucesso.")
            return
        except Exception as e:
            print(f"⏳ Tentativa {i}/{max_tries} falhou: {e}")
            await asyncio.sleep(2)
    raise Exception("🚫 Falha ao conectar ao banco após várias tentativas.")
