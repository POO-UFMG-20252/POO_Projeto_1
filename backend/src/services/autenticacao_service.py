from abc import abstractmethod

from classes.funcionario import Funcionario

class AutenticacaoService():
    @abstractmethod
    def cadastro() -> Funcionario:
        pass
    @abstractmethod
    def login(self, cpf: str, senha: str) -> bool:
        pass
    @abstractmethod
    def gerar_hash_senha(senha: str) -> str:
        pass