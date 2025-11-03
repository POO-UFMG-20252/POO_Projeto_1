from abc import abstractmethod
from typing import List, Dict, Any
from classes.produto import Produto

class CaixaService:
    @abstractmethod
    def buscar_produtos_por_nome(self, termo: str) -> List[Produto]:
        pass
    
    @abstractmethod
    def processar_venda(self, itens_venda: List[Dict[str, Any]], id_operador: int) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def obter_produto_por_id(self, id_produto: int) -> Produto:
        pass