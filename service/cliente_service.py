from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.db.cliente_model import ClienteDB
from models.schema import cliente_schema

async def create_cliente(db: AsyncSession, cliente: cliente_schema.ClienteCreate):
    db_cliente = ClienteDB(**cliente.model_dump())
    db.add(db_cliente)
    await db.commit()
    await db.refresh(db_cliente)
    return db_cliente

async def get_cliente(db: AsyncSession, cliente_id: int):
    stmt = select(ClienteDB).where(ClienteDB.id == cliente_id)
    result = await db.execute(stmt)
    return result.scalars().first()