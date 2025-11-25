from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from service.produto_service import get_produto_with_frete
from models.schema.pedido_schema import ItemCarrinho
from typing import List, Dic

async def _verificar_estoque_e_total(db: AsyncSession, itens: List[ItemCarrinho]):

    carrinho_detalhado = []
    subtotal = 0.0
    frete_total = 0.0

    for item in itens:
        produto_db = await get_produto_with_frete(db, item.produto_id)
        
    if not produto_db:
        raise HTTPException(status_code=404, detail=f"Produto ID {item.produto_id}") #DECISÃO: Impedir a compra
    
    if produto_db.estoque < item.quantidade:
        raise HTTPException(
            status_code=400, 
            detail= (f"Estoque insuficiente para {produto_db.nome}. Disponível: {produto}"))
                    
        # REPETIÇÃO: Soma
    item_subtotal = produto_db.preco * item.quantidade
    subtotal += item_subtotal
    frete_total += produto_db.frete # Frete já é polimórfico

    carrinho_detalhado.append({

        "produto_db": produto_db,
        "quantidade": item.quantidade,
        "subtotal": item_subtotal

                })
    
    return carrinho_detalhado, subtotal, frete_total

async def adicionar_item_ao_carrinho(cliente_id: int, item: ItemCarrinho):
 #Adiciona/Atualiza um item na estrutura de dados do carrinho em memória.

    if cliente_id not in CARRINHO_DE_COMPRAS:
        CARRINHO_DE_COMPRAS[cliente_id] = []
        
    for existing_item in CARRINHO_DE_COMPRAS[cliente_id]:
        
        if existing_item.produto_id == item.produto_id:
            existing_item.quantidade = item.quantidade

            return CARRINHO_DE_COMPRAS[cliente_id]
        
    CARRINHO_DE_COMPRAS[cliente_id].append(item)

    return CARRINHO_DE_COMPRAS[cliente_id]


