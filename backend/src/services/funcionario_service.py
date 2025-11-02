from abc import abstractmethod
from typing import List
from classes.funcionario import Funcionario

class FuncionarioService:
    @abstractmethod
    def cadastrar_funcionario(self, nome: str, cpf: str, email: str, data_nascimento: str, salario: float, tipo: int) -> Funcionario:
        pass
    
    @abstractmethod
    def listar_funcionarios(self) -> List[Funcionario]:
        pass
    
    @abstractmethod
    def buscar_funcionario(self, cpf: str) -> Funcionario:
        pass
    
    @abstractmethod
    def listar_subordinados(self, cpf: str):
        pass
    
    @abstractmethod
    def demitir(self, cpf_gerente: str, cpf_funcionario: str):
        pass