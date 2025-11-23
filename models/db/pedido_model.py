from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class PedidoDB(Base):

    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    total_pedido = Column(Float, nullable=False)
    total_frete = Column(Float, nullable=False)
    status = Column(String, default="Pendente")
    data_criacao = Column(DateTime, default=datetime.utcnow)
    cliente = relationship("ClienteDB", back_populates="pedidos")
    itens = relationship("ItemPedidoDB", back_populates="pedido", cascade="all, delete-orp")
                         
class ItemPedidoDB(Base):
    
    __tablename__ = "itens_pedido"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, nullable=False)
    nome_produto = Column(String, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
    pedido = relationship("PedidoDB", back_populates="itens")