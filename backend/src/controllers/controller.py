from flask import Request

from classes.custom_exception import CustomException
from services.autenticacao_service import AutenticacaoService

class Controller():
    def __init__(self, autenticacaoService: AutenticacaoService):
        self.autenticacaoService = autenticacaoService
    
    def validar_acesso(request: Request, nivel_de_acesso: int):
        try:
            bearer_token = request.headers['Authorization']
            token = bearer_token.split("Bearer ")[1]
            
        except KeyError:
            raise CustomException("Token Inválido")