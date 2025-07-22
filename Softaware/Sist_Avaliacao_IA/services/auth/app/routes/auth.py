from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm

from app.models import Login
from app.services.schemas import UserCreate, UserOut
from app.services.dependencies import get_db, get_current_user
from app.services.security import (
    verify_password,
    get_password_hash,
    create_access_token
)
from app.services.email_utils import send_confirmation_email 

from jose import JWTError, jwt
from fastapi.responses import HTMLResponse
from app.services.security import SECRET_KEY, ALGORITHM

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"message": "pong"}

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):

    # Verifica se username ou email já existem
    result = await db.execute(
        select(Login).where((Login.username == user.username) | (Login.email == user.email))
    )
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário ou e-mail já cadastrado.")

     # Cria novo usuário
    hashed_password = get_password_hash(user.password)
    db_user = Login(
        username=user.username,
        email=user.email,
        nome=user.nome,
        senha=hashed_password,
        confirmado=False  # <- assume que foi adicionado esse campo no modelo
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

     # Cria token de verificação
    token = create_access_token({"sub": user.username})

    # Envia e-mail de confirmação
    send_confirmation_email(
        to_email=user.email,
        username=user.username,
        password=user.password,
        token=token
    )

    return db_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Login).where(Login.username == form_data.username))
    user = result.scalars().first()

    if not user or not verify_password(form_data.password, user.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: Login = Depends(get_current_user)):
    return current_user

@router.get("/verify-email", response_class=HTMLResponse)
async def verify_email(token: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Token inválido.")
    except JWTError:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado.")

    # Busca usuário
    result = await db.execute(select(Login).where(Login.username == username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    if user.confirmado:
        return HTMLResponse(content="<h2>✅ E-mail já confirmado.</h2>")

    user.confirmado = True
    await db.commit()

    return HTMLResponse(content="<h2>✅ E-mail confirmado com sucesso. Você já pode fazer login!</h2>")
