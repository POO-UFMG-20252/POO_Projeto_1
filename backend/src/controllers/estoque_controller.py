from flask import Blueprint, jsonify

from classes.contoller_error import ControllerError
from controllers.controller import Controller
from services.autenticacao_service import AutenticacaoService
from services.estoque_service import EstoqueService

class EstoqueController(Controller):
    def __init__(self, nome: str, estoqueService: EstoqueService, autenticacaoService: AutenticacaoService):
        super().__init__(nome, autenticacaoService)
        self.estoque_service = estoqueService

    def registrar_rotas(self, app):
        app.add_url_rule('/api/estoque', 'buscar_estoque', self.get_estoque, methods=['GET'])
        app.add_url_rule('/api/estoque/<int:item_id>', 'buscar_produto_estoque', self.get_item_estoque, methods=['GET'])

    def get_estoque(self):
        try:
            itens = self.estoque_service.buscar_todos_itens()
            return jsonify(itens)
        except Exception as e:
            print(f"Erro ao consultar estoque: {e}")
            return jsonify(ControllerError('Erro inesperado ao consultar estoque').to_dict()), 500
        
    def get_item_estoque(self, item_id):
        try:
            item = self.estoque_service.buscar_item_por_id(item_id)
            if item:
                return jsonify(item)
            return jsonify(ControllerError('Item não encontrado')), 404
        except Exception as e:
            return jsonify(ControllerError('Erro inesperado ao consultar item do estoque').to_dict()), 500
