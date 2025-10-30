import jwt
from services.autenticacao_service import AutenticacaoService

class AutenticacaoServiceImpl(AutenticacaoService):
    def __init__(self, conexaoBancoDeDados):
        self.conexaoBancoDeDados = conexaoBancoDeDados
    
    def login(cpf: str, senha: str):
        
        
        return "fake-token"
    def validar_acesso(token: str, nivel_de_acesso: int):
        return True