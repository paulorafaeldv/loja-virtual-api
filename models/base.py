from abc import ABC, abstractmethod
# ABSTRAÇÃO para definir classes que não podem ser instanciadas diretamente e que forçam classes filhas a implementarem métodos específicos
class EntidadeLoja(ABC): # Define a primeira classe abstrata. Ao herdar de ABC, esta classe não pode ser instanciada. Ela representa o contrato básico para qualquer "entidade" principal (como Produto, Cliente, Pedido, etc.) na sua loja.
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
        self.tipo: str = "indefinido" # Adicionado: Garantir que o atributo exista
        self.frete: float = 0.0
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
        self.tipo = "digital"
        self.frete = self.calcular_frete()

    def calcular_frete(self) -> float:
        # Frete base + R$ 1.50 por kg
        return 10.00 + (self.peso * 1.50)
    
class ProdutoDigitalLogica(ProdutoEntidade):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = "digital"
        self.frete = self.calcular_frete()
    def calcular_frete(self) -> float:
        # Frete zero
        return 0.00
