from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.database import get_db
from service import cliente_service
from models.schema import cliente_schema
from models.db.cliente_model import ClienteDB
from sqlalchemy import select

@router.post("/", response_model=cliente_schema.ClienteSchema, status_code=status.HTTP_201_CREATED)
async def create_new_cliente(
 cliente: cliente_schema.ClienteCreate, db: AsyncSession = Depends(get_db)
):
 return await cliente_service.create_cliente(db, cliente)
@router.get("/{cliente_id}", response_model=cliente_schema.ClienteSchema)
async def read_cliente(cliente_id: int, db: AsyncSession = Depends(get_db)):
    db_cliente = await cliente_service.get_cliente(db, cliente_id)
    if db_cliente is None:
       raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Cliente não encontrado"
    )
    return db_cliente