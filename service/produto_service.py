from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import load_only, with_polymorphic
from models.db.produto_model import ProdutoDB, ProdutoFisicoDB, ProdutoDigitalDB
from models.schema import produto_schema
from models.base import ProdutoFisicoLogica, ProdutoDigitalLogica

def _map_db_to_logica(produto_db: ProdutoDB):
    common_attrs = {'id': produto_db.id, 'nome': produto_db.nome,
    'preco': produto_db.preco, 'estoque': produto_db.estoque}

    if hasattr(produto_db, 'peso') and produto_db.peso is not None:
        return ProdutoFisicoLogica(**common_attrs, peso=produto_db.peso)
    
    elif not hasattr(produto_db, 'peso') or produto_db.peso is None:
        # Assumindo que ProdutoDigitalDB não tem peso, se não for físico, é digital.
        return ProdutoDigitalLogica(**common_attrs)

    return None

async def get_produto_with_frete(db: AsyncSession, produto_id: int):
    """Busca o produto e aplica o POO/Polimorfismo para calcular o frete."""
    stmt = select(ProdutoDB).where(ProdutoDB.id == produto_id)
    result = await db.execute(stmt)
    produto_db = result.scalars().first()

    if not produto_db: 
        return None

    produto_logica = _map_db_to_logica(produto_db)
    return produto_logica

async def create_produto(db: AsyncSession, produto: produto_schema.ProdutoBase, tipo: str):

    dados_produto = produto.model_dump()
    if 'frete' in dados_produto:
        del dados_produto['frete']

    if tipo == "fisico":
        db_model = ProdutoFisicoDB(**dados_produto)
    elif tipo == "digital":
        db_model = ProdutoDigitalDB(**dados_produto)
    else:
        raise ValueError("Tipo de produto inválido. ")
    
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)
    return await get_produto_with_frete(db, db_model.id)