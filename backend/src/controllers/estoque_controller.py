import os
import sys
from flask import Blueprint, jsonify

from classes.contoller_error import ControllerError
from services.estoque_service import EstoqueService

class EstoqueController():
    def __init__(self, estoque_service: EstoqueService):
        self.estoque_service = estoque_service

    def registrar_rotas(self, app):
        app.add_url_rule('/api/estoque', 'buscar_estoque', self.login, methods=['GET'])
        app.add_url_rule('/api/estoque/<int:item_id>', 'buscar_produto_estoque', self.login, methods=['GET'])

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
