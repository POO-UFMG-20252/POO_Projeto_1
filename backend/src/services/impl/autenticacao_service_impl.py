import jwt
import bcrypt
from datetime import datetime, timedelta
from classes.custom_exception import CustomException
from services.autenticacao_service import AutenticacaoService
from services.funcionario_service import FuncionarioService

class AutenticacaoServiceImpl(AutenticacaoService):
    def __init__(self, funcionario_service: FuncionarioService):
        self.__funcionario_service = funcionario_service
        self.__chave_secreta = "e-segredo"
        self.__algoritmo = "HS256"
    
    def login(self, cpf: str, senha: str):
        funcionario = self.__funcionario_service.buscar_funcionario(cpf)
        
        if (funcionario == None):
            raise CustomException("Usuario nao encontrado!")
        
        if (self.__validar_senha(senha, funcionario.__senha)):
            return self.__gerar_token(funcionario.__cpf, funcionario.__nome, funcionario.__email, funcionario.__tipo)
        
        raise CustomException("Senha inválida!")
            
    def validar_acesso(self, token: str, nivel_de_acesso: int):
        try:
            payload = jwt.decode(token, self.__chave_secreta, algorithms=[self.__algoritmo])            

            if (payload["tipo"] in nivel_de_acesso):
                return {
                    'cpf': payload.get('cpf'),
                    'nome': payload.get('nome'),
                    'email': payload.get('email'),
                    'tipo': payload.get('tipo')  # 0=Gerente, 1=Repositor, 2=Caixa
                }

            raise CustomException("Usuário não autorizado a acessar essa funcionalidade")
        except jwt.ExpiredSignatureError:
            raise CustomException("Token expirado! Por favor, faça login novamente!")
        except jwt.InvalidTokenError:
            raise CustomException("Token inválido!")
    
    @staticmethod
    def gerar_hash_senha(senha: str):
        return bcrypt.hashpw(bytes(senha, 'utf-8'), bcrypt.gensalt())

    @staticmethod
    def __validar_senha(senha_recebida: str, senha_banco: str):
        return bcrypt.checkpw(bytes(senha_recebida, 'utf-8'), bytes(senha_banco, 'utf-8'))

    def __gerar_token(self, cpf: str, nome: str, email: str, tipo: int):
        payload = {
            "cpf": cpf,
            "nome": nome,
            "email": email,
            "exp": datetime.now() + timedelta(hours=4),
            "tipo": tipo
        }
        token_jwt = jwt.encode(payload, self.__chave_secreta, self.__algoritmo)
        return token_jwt