from abc import abstractmethod

class ProdutoService:
    @abstractmethod
    def adicionar_produto(id: int,nome: str, marca: str):
        pass
    @abstractmethod
    def editar_produto(id: int, nome: str, marca: str):
        pass
    @abstractmethod
    def remover_produto(id: int):
        pass
    @abstractmethod
    def busca_geral_produto():
        pass
    @abstractmethod
    def busca_produto(int:id):
        pass