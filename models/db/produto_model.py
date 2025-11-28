from sqlalchemy import Column, Integer, String, Float, ForeignKey
from config.database import Base


class ProdutoDB(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, default=0)
    tipo = Column(String, nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "produto_base", "polymorphic_on": tipo}


class ProdutoFisicoDB(ProdutoDB):
    __tablename__ = "produtos_fisicos"
    id = Column(Integer, ForeignKey("produtos.id"), primary_key=True)
    peso = Column(Float, nullable=False)
    __mapper_args__ = {"polymorphic_identity": "Fisico"}

class ProdutoDigitalDB(ProdutoDB):
    __tablename__ = "produtos_digitais"
    id = Column(Integer, ForeignKey("produtos.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "Digital"}