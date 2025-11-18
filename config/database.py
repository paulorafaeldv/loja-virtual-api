# config/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import AsyncGenerator

# Configuração para SQLite Assíncrono
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./store.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)

Base = declarative_base()

AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Função de Injeção de Dependência para FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Fornece uma sessão de banco de dados e garante seu fechamento."""
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

# Função para criar todas as tabelas (chamada em main.py)
async def init_db():
    async with engine.begin() as conn:
        # Importe todos os modelos aqui para que o Base saiba quais tabelas criar
        from models.db import produto_model, cliente_model, pedido_model
        await conn.run_sync(Base.metadata.create_all)