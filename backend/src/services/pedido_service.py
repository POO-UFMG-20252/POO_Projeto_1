from abc import abstractmethod
from typing import List
from classes.pedido import Pedido

class PedidoService:
    @abstractmethod
    def adicionar_pedido(self, id_responsavel: str, estado:int, lista_produtos: list[list[int]]) -> Pedido:
        pass

    @abstractmethod
    def editar_pedido(self, id:int, estado:int) -> Pedido:
        pass

    @abstractmethod
    def remover_pedido(self, id:int) -> Pedido:
        pass

    @abstractmethod
    def buscar_pedido(self, id : int) -> Pedido:
        pass
    
    @abstractmethod
    def listar_pedidos(self) -> List[Pedido]:
        pass

    @abstractmethod
    def alterar_estado_pedido(self, id: int, novo_estado: int) -> Pedido:
        pass