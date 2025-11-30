from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from service import pedido_service, carrinho_service
from models.schema import pedido_schema
from service.carrinho_service import CARRINHO_DE_COMPRAS

router = APIRouter(prefix="/carrinho", tags=["Carrinho e Pedidos"])

@router.post("/adicionar", status_code=status.HTTP_200_OK)

async def adicionar_item(
    cliente_id: int, 
    item: pedido_schema.ItemCarrinho,
    db: AsyncSession = Depends(get_db)
 ):

    return await carrinho_service.adicionar_item_ao_carrinho(cliente_id, item)
    #Adiciona ou atualiza um item no carrinho (em memória) do cliente.

@router.get("/{cliente_id}", response_model=list[pedido_schema.ItemCarrinho])

async def visualizar_carrinho(cliente_id: int):
 
#Visualiza o carrinho (em memória) do cliente.

    if cliente_id not in CARRINHO_DE_COMPRAS:
        return [] # Retorna lista vazia se não houver carrinho
    
    return CARRINHO_DE_COMPRAS[cliente_id]

@router.post("/finalizar", response_model=pedido_schema.PedidoSchema)

async def finalizar_compra(
    pedido_data: pedido_schema.PedidoCreate, 
    db: AsyncSession = Depends(get_db)
 ):
 #Finaliza o carrinho, verifica estoque, cria o pedido e atualiza o estoque.

 # Chama o serviço para executar toda a lógica de Decisão, Repetição e POO

    pedido_finalizado = await pedido_service.finalizar_pedido(db, pedido_data)

 # Limpa o carrinho após a finalização bem-sucedida

    if pedido_data.cliente_id in CARRINHO_DE_COMPRAS:
        del CARRINHO_DE_COMPRAS[pedido_data.cliente_id]
        
    return pedido_finalizado