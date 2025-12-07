from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select # Importar 'select'
from models.db.pedido_model import PedidoDB, ItemPedidoDB
from models.schema.pedido_schema import PedidoCreate
from service.carrinho_service import _verificar_estoque_e_total
from models.db.produto_model import ProdutoDB
from fastapi import HTTPException
from sqlalchemy.orm import selectinload # Importar 'selectinload'

async def finalizar_pedido(db: AsyncSession, pedido_data: PedidoCreate):
    """
    Cria o pedido final, registra os itens e atualiza o estoque, e o retorna serializável.
    """
    cliente_id = pedido_data.cliente_id
    itens_carrinho = pedido_data.itens

    # 1. VALIDAÇÃO E CÁLCULO
    # (Assume que _verificar_estoque_e_total retorna dados corretos)
    carrinho_detalhado, subtotal, frete_total = await _verificar_estoque_e_total(db, itens_carrinho)

    total_final = subtotal + frete_total
    
    # 2. CRIAÇÃO E FLUSH DO PEDIDO
    novo_pedido = PedidoDB(
        cliente_id=cliente_id,
        total_pedido=total_final,
        total_frete=frete_total
    )
    db.add(novo_pedido)
    await db.flush() # Obtém novo_pedido.id
    
    # Salva o ID. Isso é CRUCIAL para a re-busca pós-commit.
    pedido_id_criado = novo_pedido.id 

    # 3. CRIAÇÃO DOS ITENS E ATUALIZAÇÃO DO ESTOQUE
    for item_detalhe in carrinho_detalhado:
        produto_db = item_detalhe["produto_db"]
        quantidade = item_detalhe["quantidade"]

        item_pedido_db = ItemPedidoDB(
            pedido_id=pedido_id_criado,
            produto_id=produto_db.id,
            nome_produto=produto_db.nome,
            preco_unitario=produto_db.preco,
            quantidade=quantidade
        )
        db.add(item_pedido_db)

        # Atualização de estoque
        novo_estoque = produto_db.estoque - quantidade

        await db.execute(
            update(ProdutoDB)
            .where(ProdutoDB.id == produto_db.id)
            .values(estoque=novo_estoque) 
        )
    
    # 4. COMMIT DA TRANSAÇÃO
    await db.commit() 
    
    # 5. LEITURA GARANTIDA E SERIALIZÁVEL APÓS O COMMIT (Solução Definitiva)
    
    # Busca o objeto em uma nova query, garantindo que ele não esteja detached
    # e que o relacionamento 'itens' seja carregado (Eager Loading).
    statement = select(PedidoDB).options(
        selectinload(PedidoDB.itens)
    ).where(PedidoDB.id == pedido_id_criado)
    
    resultado = await db.execute(statement)
    pedido_final = resultado.scalar_one_or_none()
    
    if not pedido_final:
        # Se falhar aqui, o commit não funcionou ou o ID está errado.
        raise HTTPException(status_code=500, detail="Erro interno: Pedido criado, mas não pode ser lido para retorno.")

    # Objeto totalmente carregado e serializável
    return pedido_final