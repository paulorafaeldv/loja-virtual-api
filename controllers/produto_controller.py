from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List # Manter importação, mas list[] é preferível no Python 3.9+
from config.database import get_db
from service import produto_service
from models.schema import produto_schema

router = APIRouter(prefix="/produtos", tags=["Produtos"])

# 1. ROTA DE LISTAGEM (GET /produtos)
# O path deve ser "/" para que o prefixo "/produtos" resulte em /produtos
@router.get("/", response_model=list[produto_schema.ProdutoSchema])
async def read_produtos_listagem(db: AsyncSession = Depends(get_db)): # Renomeada para evitar conflito
    """Retorna a lista de todos os produtos, com frete calculado polimorficamente."""
    
    # ✅ Usa a nova função de serviço get_list_produtos (que é a correta)
    produtos = await produto_service.get_list_produtos(db)
    
    if not produtos:
        return [] # Retorna lista vazia (200 OK), que é o padrão para listagens
        
    return produtos

# 2. ROTA DE CRIAÇÃO (POST /produtos/fisico)
@router.post("/fisico", response_model=produto_schema.ProdutoSchema, status_code=status.HTTP_201_CREATED)
async def create_produto_fisico(
    produto: produto_schema.ProdutoFisicoCreate, db: AsyncSession = Depends(get_db)
    ):
        return await produto_service.create_produto(db, produto, "fisico")

# 3. ROTA DE CRIAÇÃO (POST /produtos/digital)
@router.post("/digital", response_model=produto_schema.ProdutoSchema, status_code=status.HTTP_201_CREATED)
async def create_produto_digital(
    produto: produto_schema.ProdutoDigitalCreate, db: AsyncSession = Depends(get_db)
    ):
        return await produto_service.create_produto(db, produto, "digital")

# 4. ROTA POR ID (GET /produtos/{produto_id})
@router.get("/{produto_id}", response_model=produto_schema.ProdutoSchema)
async def read_produto_por_id(produto_id: int, db: AsyncSession = Depends(get_db)): # Renomeada para clareza
    produto_db = await produto_service.get_produto_with_frete(db, produto_id)

    if not produto_db:
        # Se o produto não for encontrado, levanta 404
        raise HTTPException(status_code=404, detail="Produto não localizado.")

    return produto_db