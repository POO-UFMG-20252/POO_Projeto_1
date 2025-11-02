from flask import request, jsonify
from services.autenticacao_service import AutenticacaoService
from classes.contoller_error import ControllerError
from classes.custom_exception import CustomException
from utils.helpers import AuthUtils

class AutenticacaoController():
    def __init__(self, autenticacao_service: AutenticacaoService):
        self.autenticacao_service = autenticacao_service
        self.auth_utils = AuthUtils()
        
    def registrar_rotas(self, app):
        app.add_url_rule('/api/autenticacao/login', 'login', self.login, methods=['POST'])
        app.add_url_rule('/api/autenticacao/usuario', 'get_usuario', self.get_usuario, methods=['GET'])
        
    def login(self):
        data = request.get_json()
    
        # Validações básicas
        required_fields = ['cpf', 'senha']
        for field in required_fields:
            if not data.get(field):
                return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400
            
        try:
            token = self.autenticacao_service.login(data['cpf'], data['senha'])
            return jsonify({'token': token})
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            return jsonify(ControllerError('Erro inesperado ao fazer login').to_dict()), 500
        
    def get_usuario(self):
        try:
            usuario = self.auth_utils.get_usuario_logado()
            if not usuario:
                return jsonify(ControllerError('Usuário não autenticado').to_dict()), 401
            
            return jsonify(usuario)
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro ao buscar usuário: {e}")
            return jsonify(ControllerError('Erro inesperado').to_dict()), 500
