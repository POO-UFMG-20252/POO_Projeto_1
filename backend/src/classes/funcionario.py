from datetime import date

class Funcionario:
    def __init__(self, cpf: str, nome: str, data_admissao: str, 
                 email: str = "", senha: str = "", data_nascimento: str = "",
                 salario: float = 0, tipo: int = 0, ativo: bool = True, 
                 id_supervisor: int = 0):
        self.cpf = cpf
        self.nome = nome
        self.data_admissao = data_admissao
        self.email = email
        self.senha = senha
        self.data_nascimento = data_nascimento
        self.salario = salario
        self.tipo = tipo
        self.ativo = ativo
        self.id_supervisor = id_supervisor

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
    def data_admissao(self):
        return self._data_admissao

    @data_admissao.setter
    def data_admissao(self, valor):
        self._data_admissao = valor

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

    def to_dict(self):
        return {
            'cpf': self.cpf,
            'nome': self.nome,
            'data_admissao': self.data_admissao
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
            ativo=data.get('ativo', True),
            id_supervisor=data.get('id_supervisor', 0)
        )