from abc import abstractmethod
from typing import List

from classes.estoque import Estoque

class EstoqueService():
    @abstractmethod
    def buscar_todos_itens(self) -> List[Estoque]:
        pass
    @abstractmethod
    def buscar_produto_por_id(self, id: str) -> Estoque:
        pass