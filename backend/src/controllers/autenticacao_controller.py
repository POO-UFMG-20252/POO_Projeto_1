from flask import Blueprint, request, jsonify
from services.autenticacao_service import AutenticacaoService
from classes.contoller_error import ControllerError

class AutenticacaoController():
    def __init__(self, autenticacaoService: AutenticacaoService):
        self.autenticacaoService = autenticacaoService
        
    def registar_rotas(self, app):
        app.add_url_rule('/autenticacao/login', 'login', self.login, methods=['POST'])
        
    def login(self):
        data = request.get_json()
    
        cpf = data.get('cpf')
        senha = data.get('senha')
    
        if not cpf:
            return jsonify(ControllerError('CPF é obrigatório').to_dict()), 400
        if not senha:
            return jsonify(ControllerError('Senha é obrigatório').to_dict()), 400
    
        try:
            self.autenticacaoService.login(cpf, senha)
        except:
            return jsonify(ControllerError('Erro inesperado ao fazer login').to_dict()), 400
