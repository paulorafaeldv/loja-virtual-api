from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from config.database import get_db
from service import produto_service
from models.schemas import produto_schema
from models.db.produto_model import ProdutoDB
from sqlalchemy import select
import asyncio

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/fisico", response_model=produto_schema.ProdutoSchema, status_code=status.HTTP_201_CREATED)
async def create_produto_fisico(
    produto: produto_schema.ProdutoFisicoCreate, db: AsyncSession = Depends(get_db)
    ):
        return await produto_service.create_produto(db, produto, "fisico")

@router.post("/digital", response_model=produto_schema.ProdutoSchema, status_code=status.HTTP_201_CREATED)
async def create_produto_digital(
    produto: produto_schema.ProdutoDigitalCreate, db: AsyncSession = Depends(get_db)
    ):
        return await produto_service.create_produto(db, produto, "digital")

@router.get("/{produto_id}", response_model=produto_schema.ProdutoSchema)
async def read_produto(produto_id: int, db: AsyncSession = Depends(get_db)):
    produto_db = await produto_service.get_produto_with_frete(db, produto_id)

    if not produto_db:
        raise HTTPException(status_code=404, detail="Produto não localizado. ")

    return produto_db

@router.get("/", response_model=List[produto_schema.ProdutoSchema])
async def read_produtos(db: AsyncSession = Depends(get_db)):
    stmt = select(ProdutoDB)
    result = await db.execute(stmt)
    produtos_db = result.scalars().all() 

    tasks = [
        produto_service.get_produto_with_frete(db, p.id) for p in produtos_db 
    ]

    produtos_com_frete = await asyncio.gather(*tasks)

    return produtos_com_frete