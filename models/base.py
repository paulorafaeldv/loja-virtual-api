from abc import ABC, abstractmethod
# ABSTRAÇÃO
class EntidadeLoja(ABC):
    """Classe Abstrata base para todas as entidades principais."""
    @abstractmethod
    def obter_resumo(self) -> str:
        pass

# CLASSE BASE PARA POLIMORFISMO
class ProdutoEntidade(EntidadeLoja):
    """Base para Herança de Produto e Polimorfismo de Frete."""
    def __init__(self, id: int, nome: str, preco: float, estoque: int, **kwargs):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
    @abstractmethod
    def calcular_frete(self) -> float:
        """Método polimórfico: custo do frete."""
        pass
    def obter_resumo(self) -> str:
        return f"Produto: {self.nome} - Preço: R${self.preco:.2f}"
 
# HERANÇA E POLIMORFISMO (Lógica de Frete)
class ProdutoFisicoLogica(ProdutoEntidade):
    def __init__(self, peso: float, **kwargs):
        super().__init__(**kwargs)
        self.peso = peso

    def calcular_frete(self) -> float:
        # Frete base + R$ 1.50 por kg
        return 10.00 + (self.peso * 1.50)
class ProdutoDigitalLogica(ProdutoEntidade):
    def calcular_frete(self) -> float:
        # Frete zero
        return 0.00
