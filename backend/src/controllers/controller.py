from flask import Request

from classes.custom_exception import CustomException
from services.autenticacao_service import AutenticacaoService

class Controller():    
    def __init__(self, nome: str, autenticacaoService: AutenticacaoService):
        self.nome = nome
        self.autenticacaoService = autenticacaoService
    
    def _get_usuario_logado(self, request: Request, nivel_de_acesso: int):
        try:
            bearer_token = request.headers['Authorization']
            token = bearer_token.split("Bearer ")[1]
            return self.autenticacaoService.validar_acesso(token, nivel_de_acesso)
        except KeyError:
            raise CustomException("Token Inválido")