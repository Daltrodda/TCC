from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import JWTError, jwt

from app.database import SessionLocal
from app.models import Login
from app.services.security import SECRET_KEY, ALGORITHM

# OAuth2 para extração do token do header Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Dependência padrão de sessão do banco
async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

# Dependência que retorna o usuário autenticado via token
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Login:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(Login).where(Login.username == username))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user
