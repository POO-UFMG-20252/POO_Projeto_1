from abc import abstractmethod

from classes.pedido import Pedido

class PedidoService:
    @abstractmethod
    def criar_pedido(self, id_responsavel: str, estado:int, lista_produtos: list[list[int]]) -> Pedido:
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