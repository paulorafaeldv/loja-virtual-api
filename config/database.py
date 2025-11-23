from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import AsyncGenerator
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./store.db"
engine = create_async_engine(
 SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)
Base = declarative_base()
AsyncSessionLocal = sessionmaker(
 autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
async def init_db():
    async with engine.begin() as conn:
 # Importe todos os modelos para que a Base possa criar as tabelas
        from models.db import produto_model, cliente_model, pedido_model
        await conn.run_sync(Base.metadata.create_all)