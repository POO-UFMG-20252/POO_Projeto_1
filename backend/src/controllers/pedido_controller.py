from flask import jsonify, request

from classes.contoller_error import ControllerError
from classes.custom_exception import CustomException
from controllers.controller import Controller
from services.autenticacao_service import AutenticacaoService
from services.pedido_service import PedidoService

class PedidoController(Controller):
    def __init__(self, nome: str, pedido_service: PedidoService, autenticacaoService: AutenticacaoService):
        super().__init__(nome, autenticacaoService)
        self.__pedido_service = pedido_service
    
    def registrar_rotas(self, app):
        app.add_url_rule('/api/pedido', 'criar_pedido', self.criar_pedido, methods=['POST'])
        app.add_url_rule('/api/pedido', 'editar_pedido', self.editar_pedido, methods=['PUT'])
        app.add_url_rule('/api/pedido/<int:id>', 'remover_pedido', self.remover_pedido, methods=['DELETE'])
        app.add_url_rule('/api/pedido/<int:id>', 'buscar_pedido', self.buscar_pedido, methods=['GET'])

    def criar_pedido(self):
        try:
            data = request.get_json()
    
            # Validações básicas
            required_fields = ['id_responsavel', 'estado']
            for field in required_fields:
                if not data.get(field):
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400
            
            self.__pedido_service.criar_pedido(data.get('id_responsavel'), data.get('estado'))
        
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado na criacao de pedido: {e}")
            return jsonify(ControllerError('Erro inesperado ao criar pedido').to_dict()), 500
            
    def editar_pedido(self):
        try:
            data = request.get_json()
    
            # Validações básicas
            required_fields = ['id', 'estado']
            for field in required_fields:
                if not data.get(field):
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400
            
            return self.__pedido_service.editar_pedido(data.get('id'), data.get('estado'))
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado na edicao de pedido: {e}")
            return jsonify(ControllerError('Erro inesperado ao editar pedido').to_dict()), 500
    
    def remover_pedido(self, id):
        try:
            if not id:
                raise(CustomException("Id inválido"))
            
            return self.__pedido_service.remover_pedido(id)
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado na edicao de pedido: {e}")
            return jsonify(ControllerError('Erro inesperado ao editar pedido').to_dict()), 500
    
    def buscar_pedido(self, id):
        try:
            if not id:
                raise(CustomException("Id inválido"))
            
            return self.__pedido_service.buscar_pedido(id)
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado na edicao de pedido: {e}")
            return jsonify(ControllerError('Erro inesperado ao editar pedido').to_dict()), 500

        
