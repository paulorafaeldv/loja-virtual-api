from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteSchema(ClienteBase):
    id: int
    data_cadastro: datetime

class Config:
    from_attributes = True