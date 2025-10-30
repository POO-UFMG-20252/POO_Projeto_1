from abc import abstractmethod

class AutenticacaoService():
    @abstractmethod
    def cadastro():
        pass
    @abstractmethod
    def login(self, cpf: str, senha: str):
        pass