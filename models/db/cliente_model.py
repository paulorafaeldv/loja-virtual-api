from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class ClienteDB(Base):
 __tablename__ = "clientes"

 id = Column(Integer, primary_key=True, index=True)
 nome = Column(String, index=True, nullable=False)
 email = Column(String, unique=True, index=True, nullable=False)
 data_cadastro = Column(DateTime, default=datetime.utcnow)

 pedidos = relationship("PedidoDB", back_populates="cliente") # relacionamento com pedidos (1:N)
