from abc import abstractmethod

from classes.pedido import Pedido

class PedidoService:
    @abstractmethod
    def criar_pedido(id_responsavel:KeyboardInterrupt, estado:int) -> Pedido:
        pass

    @abstractmethod
    def editar_pedido(id:int, estado:int) -> Pedido:
        pass

    @abstractmethod
    def remover_pedido(id:int) -> Pedido:
        pass

    @abstractmethod
    def buscar_pedido(id : int) -> Pedido:
        pass