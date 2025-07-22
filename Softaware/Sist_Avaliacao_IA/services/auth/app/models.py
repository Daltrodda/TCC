import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base  # ajuste no import para ser absoluto (evita erro em produção)


class Login(Base):
    __tablename__ = "login"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    senha = Column(String, nullable=False)
    criado = Column(DateTime, default=datetime.utcnow)

    email_verificado = Column(Boolean, default=False)
    token_verificacao = Column(String, nullable=True)
