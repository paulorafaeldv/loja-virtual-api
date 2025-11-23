from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ItemCarrinho(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)

class ItemPedidoSchema(BaseModel):
    produto_id: int
    nome_produto: str
    preco_unitario: float
    quantidade: int

    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    cliente_id: int
    itens: List[ItemCarrinho]

class PedidoSchema(BaseModel):
    id: int
    cliente_id: int
    data_criacao: datetime
    status: str
    total_pedido: float
    total_frete: float
    itens: List[ItemPedidoSchema]

    class Config:
        from_attributes = True
 


