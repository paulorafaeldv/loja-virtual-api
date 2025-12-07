from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime
from typing import List 

class PedidoDB(Base):

    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    total_pedido = Column(Float, nullable=False)
    total_frete = Column(Float, nullable=False)
    status = Column(String, default="Pendente")
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    cliente = relationship("ClienteDB", back_populates="pedidos")
    
    # ⚠️ SEM lazy="selectin". O service fará o carregamento na re-busca.
    itens = relationship(
        "ItemPedidoDB", 
        back_populates="pedido", 
        cascade="all, delete-orphan" 
    )
                            
class ItemPedidoDB(Base):
    
    __tablename__ = "itens_pedido"
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, nullable=False)
    nome_produto = Column(String, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)
    
    pedido = relationship("PedidoDB", back_populates="itens")