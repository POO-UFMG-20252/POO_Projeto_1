import jwt
import bcrypt
from datetime import datetime, timedelta
from classes.custom_exception import CustomException
from services.autenticacao_service import AutenticacaoService
from services.funcionario_service import FuncionarioService

class AutenticacaoServiceImpl(AutenticacaoService):
    def __init__(self, funcionario_service: FuncionarioService):
        self.funcionario_service = funcionario_service
        self.chave_secreta = "e-segredo"
        self.algoritmo = "HS256"
    
    def login(self, cpf: str, senha: str):
        funcionario = self.funcionario_service.buscar_funcionario(cpf)
        
        if (funcionario == None):
            raise CustomException("Usuario nao encontrado!")
        
        if (self._validar_senha(senha, funcionario.senha)):
            return self._gerar_token(funcionario.cpf, funcionario.nome, funcionario.email, funcionario.tipo)
        
        raise CustomException("Senha inválida!")
            
    def validar_acesso(self, token: str, nivel_de_acesso: int):
        try:
            payload = jwt.decode(token, self.chave_secreta, algorithms=[self.algoritmo])
        
            if isinstance(nivel_de_acesso, list):
                return payload["tipo"] in nivel_de_acesso
            else:
                return payload["tipo"] == nivel_de_acesso
        except jwt.ExpiredSignatureError:
            raise CustomException("Token expirado! Por favor, faça login novamente!")
        except jwt.InvalidTokenError:
            raise CustomException("Token inválido!")
    
    @staticmethod
    def gerar_hash_senha(senha: str):
        return bcrypt.hashpw(bytes(senha, 'utf-8'), bcrypt.gensalt())

    @staticmethod
    def _validar_senha(senha_recebida: str, senha_banco: str):
        if (senha_banco == senha_recebida):
            return True

    def _gerar_token(self, cpf: str, nome: str, email: str, tipo: int):
        payload = {
            "cpf": cpf,
            "nome": nome,
            "email": email,
            "exp": datetime.now() + timedelta(hours=4),
            "tipo": tipo
        }
        token_jwt = jwt.encode(payload, self.chave_secreta, self.algoritmo)
        return token_jwt