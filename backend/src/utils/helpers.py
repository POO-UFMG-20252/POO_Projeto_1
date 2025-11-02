import jwt
from flask import request, jsonify
from classes.custom_exception import CustomException

class AuthUtils:
    def __init__(self):
        self.chave_secreta = "e-segredo"
        self.algoritmo = "HS256"
    
    def get_usuario_logado(self):
        """Retorna os dados do usuário logado a partir do token"""
        token = request.headers.get('Authorization')
        
        if not token or not token.startswith('Bearer '):
            return None
        
        try:
            token = token.replace('Bearer ', '')
            payload = jwt.decode(token, self.chave_secreta, algorithms=[self.algoritmo])
            return {
                'cpf': payload.get('cpf'),
                'nome': payload.get('nome'),
                'email': payload.get('email'),
                'tipo': payload.get('tipo')  # 0=Gerente, 1=Repositor, 2=Caixa
            }
        except jwt.ExpiredSignatureError:
            raise CustomException("Token expirado")
        except jwt.InvalidTokenError:
            raise CustomException("Token inválido")
        except Exception as e:
            print(f"Erro ao decodificar token: {e}")
            return None
    
    def verificar_acesso(self, tipos_permitidos):
        """Verifica se o usuário tem acesso baseado no tipo"""
        usuario = self.get_usuario_logado()
        if not usuario:
            raise CustomException("Usuário não autenticado")
        
        if usuario['tipo'] not in tipos_permitidos:
            raise CustomException("Acesso negado")
        
        return usuario