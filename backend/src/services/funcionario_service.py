from abc import abstractmethod

class FuncionarioService:
    @abstractmethod
    def cadastrar_funcionario(self, cpf: str):
        pass
    
    @abstractmethod
    def buscar_funcionario(self, cpf: str):
        pass
    
    @abstractmethod
    def demitir(self, cpf_gerente: str, cpf_funcionario: str):
        pass