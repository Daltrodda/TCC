from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    nome: str
    password: str

class UserOut(BaseModel):
    id: str
    username: str
    email: str
    nome: str
    criado: datetime

    class Config:
        orm_mode = True
