from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, with_polymorphic 
from models.db.produto_model import ProdutoDB, ProdutoFisicoDB, ProdutoDigitalDB
from models.schema import produto_schema
from models.base import ProdutoFisicoLogica, ProdutoDigitalLogica

def _map_db_to_logica(produto_db: ProdutoDB):
    common_attrs = {'id': produto_db.id, 'nome': produto_db.nome,
    'preco': produto_db.preco, 'estoque': produto_db.estoque}

    # Esta lógica depende da disponibilidade imediata do atributo 'peso'
    if hasattr(produto_db, 'peso') and produto_db.peso is not None:
        return ProdutoFisicoLogica(**common_attrs, peso=produto_db.peso)
    
    elif not hasattr(produto_db, 'peso') or produto_db.peso is None:
        return ProdutoDigitalLogica(**common_attrs)

    return None

# 🌟 FUNÇÃO CORRIGIDA (GET por ID) 🌟
async def get_produto_with_frete(db: AsyncSession, produto_id: int):
    """Busca o produto aplicando o Polimorfismo e o carregamento ansioso."""
    
    produto_polimorfico = with_polymorphic(
        ProdutoDB, 
        [ProdutoFisicoDB, ProdutoDigitalDB]
    )

    stmt = (
        select(produto_polimorfico)
        .where(ProdutoDB.id == produto_id)
        # ✅ SOLUÇÃO: Força o carregamento do 'peso' na primeira consulta
        .options(selectinload('*')) 
    )
    
    result = await db.execute(stmt)
    produto_db = result.unique().scalars().first()

    if not produto_db: 
        return None

    produto_logica = _map_db_to_logica(produto_db)
    return produto_logica


# 🌟 FUNÇÃO NOVA (GET de Lista) 🌟
async def get_list_produtos(db: AsyncSession):
    """Busca a lista completa de produtos aplicando o Polimorfismo (Frete)."""
    
    produto_polimorfico = with_polymorphic(
        ProdutoDB, 
        [ProdutoFisicoDB, ProdutoDigitalDB]
    )

    # Consulta que busca todos os produtos com carregamento ansioso
    stmt = (
        select(produto_polimorfico)
        .options(selectinload('*')) # ✅ ESSENCIAL para carregamento assíncrono de lista polimórfica
    )
    
    result = await db.execute(stmt)
    
    # unique() e scalars() são importantes para resolver o polimorfismo corretamente
    produtos_db = result.unique().scalars().all()

    if not produtos_db:
        return []

    # Mapeamento Síncrono para a Lógica de Negócio (agora seguro, pois o 'peso' está carregado)
    produtos_logica = [_map_db_to_logica(p) for p in produtos_db]
    
    return produtos_logica


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
    # A chamada aqui usa a função CORRIGIDA
    return await get_produto_with_frete(db, db_model.id)