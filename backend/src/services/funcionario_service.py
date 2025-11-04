from abc import abstractmethod
from typing import List

from classes.funcionario import Funcionario

class FuncionarioService:
    @abstractmethod
    def cadastrar_funcionario(self, nome: str, cpf: str, email: str, senha: str, data_nascimento: str, salario: float, tipo: str) -> Funcionario:
        pass
    
    @abstractmethod
    def listar_funcionarios(self) -> List[Funcionario]:
        pass
    
    @abstractmethod
    def buscar_funcionario(self, cpf: str) -> Funcionario:
        pass
    
    @abstractmethod
    def demitir(self, cpf_funcionario: str, motivo: str) -> Funcionario:
        pass