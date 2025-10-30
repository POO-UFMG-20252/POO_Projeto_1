from abc import abstractmethod

class PedidoService:
    @abstractmethod
    def criar_pedido(id: int, id_responsavel:int,id_mercado:int,estado:int):
        pass

    @abstractmethod
    def editar_pedido(id:int, estado:int):
        pass

    @abstractmethod
    def remover_pedido(id:int):
        pass