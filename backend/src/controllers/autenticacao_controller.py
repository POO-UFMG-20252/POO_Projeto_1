from flask import request, jsonify
from services.autenticacao_service import AutenticacaoService
from classes.contoller_error import ControllerError
from classes.custom_exception import CustomException

class AutenticacaoController():
    def __init__(self, autenticacao_service: AutenticacaoService):
        self.autenticacao_service = autenticacao_service
        
    def registrar_rotas(self, app):
        app.add_url_rule('/api/autenticacao/login', 'login', self.login, methods=['POST'])
        
    def login(self):
        data = request.get_json()
    
        cpf = data.get('cpf')
        senha = data.get('senha')
    
        if not cpf:
            return jsonify(ControllerError('CPF é obrigatório').to_dict()), 400
        if not senha:
            return jsonify(ControllerError('Senha é obrigatório').to_dict()), 400
    
        try:
            token = self.autenticacao_service.login(cpf, senha)
            return jsonify({'token': token})
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            return jsonify(ControllerError('Erro inesperado ao fazer login').to_dict()), 500
