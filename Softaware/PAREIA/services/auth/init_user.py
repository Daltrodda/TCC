from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum
import enum
from passlib.context import CryptContext
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/appdb")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class PerfilEnum(enum.Enum):
    Aluno = "Aluno"
    Responsavel = "Responsavel"
    Coordenacao = "Coordenacao"
    Professor = "Professor"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    email = Column(String, nullable=False)
    perfil = Column(Enum(PerfilEnum), nullable=False)

Base.metadata.create_all(bind=engine)
db = SessionLocal()

usuario = User(
    nome="Daltro Araujo",
    login="daltro2005",
    senha=pwd_context.hash("daltro123"),
    email="daltro2005@gmail.com",
    perfil=PerfilEnum.Coordenacao
)

if not db.query(User).filter_by(login=usuario.login).first():
    db.add(usuario)
    db.commit()
    print("Usuário inicial criado.")
else:
    print("Usuário já existe.")
