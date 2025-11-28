from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update
from models.db.pedido_model import PedidoDB, ItemPedidoDB
from models.schema.pedido_schema import PedidoCreate
from service.carrinho_service import _verificar_estoque_e_total
from models.db.produto_model import ProdutoDB
from fastapi import HTTPException

async def finalizar_pedido(db: AsyncSession, pedido_data: PedidoCreate):
    """
    Cria o pedido final, registra os itens e atualiza o estoque.
    """
    cliente_id = pedido_data.cliente_id
    itens_carrinho = pedido_data.itens

    carrinho_detalhado, subtotal, frete_total = await _verificar_estoque_e_total(db, itens_carrinho)

    total_final = subtotal + frete_total
    # CRIAÇÃO DO PEDIDO
    novo_pedido = PedidoDB(
    cliente_id=cliente_id,
    total_pedido=total_final,
    total_frete=frete_total
    )
    db.add(novo_pedido)
    await db.flush()
    # CRIAÇÃO DOS ITENS E ATUALIZAÇÃO DO ESTOQUE
    for item_detalhe in carrinho_detalhado:
        produto_db = item_detalhe["produto_db"]
        quantidade = item_detalhe["quantidade"]

        item_pedido_db = ItemPedidoDB(
        pedido_id=novo_pedido.id,
        produto_id=produto_db.id,
        nome_produto=produto_db.nome,
        preco_unitario=produto_db.preco,
        quantidade=quantidade
    )
    db.add(item_pedido_db)

    # ATUALIZAÇÃO DE ESTOQUE (DECREMENTO)
    novo_estoque = produto_db.estoque - quantidade

    await db.execute(
    update(ProdutoDB)
    .where(ProdutoDB.id == produto_db.id)
    )
    b.commit()
    await db.refresh(novo_pedido)
    return novo_pedido

