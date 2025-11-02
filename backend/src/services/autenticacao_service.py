from abc import abstractmethod

from classes.funcionario import Funcionario

class AutenticacaoService():
    @abstractmethod
    def cadastro() -> Funcionario:
        pass
    @abstractmethod
    def login(self, cpf: str, senha: str) -> str:
        pass
    @abstractmethod
    def validar_acesso(self, token: str, nivel_de_acesso: int) -> bool:
        pass
    
    @staticmethod
    @abstractmethod
    def gerar_hash_senha(senha: str) -> str:
        pass