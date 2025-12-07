from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import AsyncGenerator
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./store.db"
engine = create_async_engine(
 SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)
Base = declarative_base()
AsyncSessionLocal = sessionmaker( #criando objetos assincronos 
 autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

async def get_db() -> AsyncGenerator[AsyncSession, None]: #função de dependencia
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

async def init_db(): #função de inicialização
    async with engine.begin() as conn:
        from models.db import produto_model, cliente_model, pedido_model
        await conn.run_sync(Base.metadata.create_all)