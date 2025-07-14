from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, models, auth
from pydantic import BaseModel

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

class LoginRequest(BaseModel):
    login: str
    senha: str

@app.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(database.SessionLocal)):
    user = db.query(models.User).filter(models.User.login == request.login).first()
    if not user or not auth.verify_password(request.senha, user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = auth.create_access_token({"sub": user.login, "perfil": user.perfil.value, "nome": user.nome})
    return {"access_token": token, "perfil": user.perfil.value, "nome": user.nome}

@app.get("/health")
def health():
    return {"status": "auth service ok"}

from .models import User, PerfilEnum
from fastapi import HTTPException

class RegisterRequest(BaseModel):
    nome: str
    login: str
    senha: str
    email: str
    perfil: PerfilEnum

@app.post("/register")
def register_user(request: RegisterRequest, db: Session = Depends(database.SessionLocal)):
    existing = db.query(User).filter(User.login == request.login).first()
    if existing:
        raise HTTPException(status_code=400, detail="Login já cadastrado.")
    hashed = auth.hash_password(request.senha)
    new_user = User(
        nome=request.nome,
        login=request.login,
        senha=hashed,
        email=request.email,
        perfil=request.perfil
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Usuário cadastrado com sucesso"}
