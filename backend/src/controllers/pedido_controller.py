from controllers.controller import Controller
from services.autenticacao_service import AutenticacaoService
from services.pedido_service import PedidoService

class PedidoController(Controller):
    def __init__(self, nome: str, pedido_service: PedidoService, autenticacaoService: AutenticacaoService):
        super().__init__(nome, autenticacaoService)
        self.pedido_service = pedido_service
    
    def registrar_rotas(self, app):
        app.add_url_rule('/api/pedido', 'criar_pedido', self.criar_pedido, methods=['POST'])
        app.add_url_rule('/api/pedido', 'editar_pedido', self.editar_pedido, methods=['PUT'])
        app.add_url_rule('/api/pedido/<int:id>', 'remover_pedido', self.remover_pedido, methods=['DELETE'])
        app.add_url_rule('/api/pedido/<int:id>', 'buscar_pedido', self.buscar_pedido, methods=['GET'])

    def criar_pedido(self):
        pass
    def editar_pedido(self):
        pass
    def remover_pedido(self, id):
        pass
    def buscar_pedido(self, id):
        pass
        
