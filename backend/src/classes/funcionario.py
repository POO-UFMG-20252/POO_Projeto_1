from datetime import date

class Funcionario:
    def __init__(self, cpf: str, nome: str, data_admissao: str, 
                email: str = "", senha: str = "", data_nascimento: str = "",
                salario: float = 0, tipo: int = 0, ativo: bool = True, motivo_demissao: str = ""):
        self.__cpf = cpf
        self.__nome = nome
        self.__data_admissao = data_admissao
        self.__email = email
        self.__senha = senha
        self.__data_nascimento = data_nascimento
        self.__salario = salario
        self.__tipo = tipo
        self.__ativo = ativo
        self.__motivo_demissao = motivo_demissao

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, valor):
        self.__cpf = valor

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        self.__nome = valor

    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, valor):
        self.__senha = valor

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, valor):
        self.__email = valor

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, valor):
        self.__data_nascimento = valor

    @property
    def data_admissao(self):
        return self.__data_admissao

    @data_admissao.setter
    def data_admissao(self, valor):
        self.__data_admissao = valor

    @property
    def salario(self):
        return self.__salario

    @salario.setter
    def salario(self, valor):
        self.__salario = valor

    @property
    def tipo(self):
        return self.__tipo
    
    @tipo.setter
    def tipo(self, valor):
        self.__tipo = valor

    @property
    def ativo(self):
        return self.__ativo

    @ativo.setter
    def ativo(self, valor):
        self.__ativo = valor

    @property
    def motivo_demissao(self):
        return self.__motivo_demissao

    @motivo_demissao.setter
    def motivo_demissao(self, valor):
        self.__motivo_demissao = valor

    def to_dict(self):
        return {
            'cpf': self.__cpf,
            'nome': self.__nome,
            'data_admissao': self.__data_admissao,
            'tipo': self.__tipo
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Método alternativo para criar Funcionario a partir de um dicionário"""
        return cls(
            cpf=data.get('cpf', ''),
            nome=data.get('nome', ''),
            data_admissao=data.get('data_admissao', ''),
            email=data.get('email', ''),
            senha=data.get('senha', ''),
            data_nascimento=data.get('data_nascimento', ''),
            salario=data.get('salario', 0),
            tipo=data.get('tipo', 0),
            ativo=data.get('ativo', True)
        )