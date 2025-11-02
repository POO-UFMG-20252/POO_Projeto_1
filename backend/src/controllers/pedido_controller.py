class PedidoController():
    def __init__(self, pedido_service: PedidoService):
        self.pedido_service = pedido_service
    
    def registrar_rotas(self, app):
        app.add_url_rule('/api/estoque', 'buscar_estoque', self.login, methods=['GET'])
        app.add_url_rule('/api/estoque/<int:item_id>', 'buscar_produto_estoque', self.login, methods=['GET'])
