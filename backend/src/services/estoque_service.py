from abc import abstractmethod
from typing import List, Dict, Any
from classes.produto import Produto
from classes.estoque import ItemEstoque  

class EstoqueService:
    @abstractmethod
    def listar_produtos(self) -> List[Produto]:
        pass
    
    @abstractmethod
    def listar_estoque_armazem(self, id_mercado: int = 1) -> List[ItemEstoque]:
        pass
    
    @abstractmethod
    def listar_estoque_loja(self, id_mercado: int = 1) -> List[ItemEstoque]:
        pass
    
    @abstractmethod
    def obter_visualizacao_estoque(self, id_mercado: int = 1) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def mover_produto(self, id_item: int, novo_pos_x: int, novo_pos_y: int, novo_local: str) -> bool:
        pass
    
    @abstractmethod
    def adicionar_produto(self, id_produto: int, id_mercado: int, pos_x: int, pos_y: int, 
                         quantidade: int, local: str) -> bool:
        pass
    
    @abstractmethod
    def remover_produto(self, id_item: int) -> bool:
        pass