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
    from_attributes = True # instrui o Pydantic a tentar ler os dados não apenas como um dicionário (acesso via ['chave']), mas também como atributos de um objeto (acesso via .atributo).