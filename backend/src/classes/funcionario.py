from datetime import date

class Funcionario:
    def __init__(self, cpf: str, nome: str, senha: str, email: str, data_nascimento: date, salario: float, tipo: int, ativo: bool, id_supervisor: int = None, motivo_demissao: str = None):
        self._cpf = cpf
        self._nome = nome
        self._senha = senha
        self._email = email
        self._data_nascimento = data_nascimento
        self._salario = salario
        self._tipo = tipo
        self._ativo = ativo
        self._id_supervisor = id_supervisor
        self._motivo_demissao = motivo_demissao

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        self._cpf = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, valor):
        self._senha = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        self._email = valor

    @property
    def data_nascimento(self):
        return self._data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, valor):
        self._data_nascimento = valor

    @property
    def salario(self):
        return self._salario

    @salario.setter
    def salario(self, valor):
        self._salario = valor

    @property
    def tipo(self):
        return self._tipo
    
    @tipo.setter
    def tipo(self, valor):
        self._tipo = valor

    @property
    def ativo(self):
        return self._ativo

    @ativo.setter
    def ativo(self, valor):
        self._ativo = valor

    @property
    def id_supervisor(self):
        return self._id_supervisor

    @id_supervisor.setter
    def id_supervisor(self, valor):
        self._id_supervisor = valor

    @property
    def motivo_demissao(self):
        return self._motivo_demissao

    @motivo_demissao.setter
    def motivo_demissao(self, valor):
        self._motivo_demissao = valor