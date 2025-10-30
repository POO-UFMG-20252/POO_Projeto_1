from abc import abstractmethod

class ProdutoService:
    @abstractmethod
    def adicionar(nome: str, marca: str):
        pass
    @abstractmethod
    def editar(id: int, nome: str, marca: str):
        pass
    @abstractmethod
    def remover(id: int):
        pass