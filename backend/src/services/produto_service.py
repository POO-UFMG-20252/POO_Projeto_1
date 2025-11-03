from abc import abstractmethod

from classes.produto import Produto
from typing import List

class ProdutoService:
    @abstractmethod
    def adicionar_produto(nome: str, marca: str, preco: float) -> Produto:
        pass
    @abstractmethod
    def editar_produto(id: int, nome: str, marca: str) -> Produto:
        pass
    @abstractmethod
    def remover_produto(id: int) -> Produto:
        pass
    @abstractmethod
    def busca_geral_produto() -> list[Produto]:
        pass
    @abstractmethod
    def busca_produto(int:id) -> Produto:
        pass
    @abstractmethod
    def buscar_produtos_por_nome(self, termo: str) -> List[Produto]:
        pass