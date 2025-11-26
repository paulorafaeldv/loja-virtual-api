from pydantic import BaseModel, Field
class ProdutoBase(BaseModel):
    nome: str
    preco: float = Field(..., gt=0)
    estoque: int = Field(..., ge=0)
class ProdutoFisicoCreate(ProdutoBase):
    peso: float = Field(..., gt=0)

class ProdutoDigitalCreate(ProdutoBase):
    pass   

class ProdutoDigitalCreate(ProdutoBase):
    id: int
    tipo: str
    frete: float = Field(..., description = "custo do frete calculado por Polimorfismo. ")

class config:
    from_attributes = True  