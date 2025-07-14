from .database import Base
from sqlalchemy import Column, Integer, String, Enum
import enum

class PerfilEnum(enum.Enum):
    Aluno = "Aluno"
    Responsavel = "Responsavel"
    Coordenacao = "Coordenacao"
    Professor = "Professor"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False, index=True)
    senha = Column(String, nullable=False)
    email = Column(String, nullable=False)
    perfil = Column(Enum(PerfilEnum), nullable=False)
