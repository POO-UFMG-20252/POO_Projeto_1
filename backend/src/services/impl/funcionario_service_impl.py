from datetime import date
from sqlite3 import Connection
from classes.funcionario import Funcionario
from database.connection import DatabaseConnection
from services.funcionario_service import FuncionarioService

class FuncionarioServiceImpl(FuncionarioService):
    def __init__(self, banco_de_dados: DatabaseConnection):
        self.banco_de_dados = banco_de_dados
        
    def cadastrar_funcionario(self, cpf: str):
        pass
    
    def buscar_funcionario(self, cpf: str):
        conexao_db = self.banco_de_dados.get_connection()
        cursor = conexao_db.cursor()

        cursor.execute("SELECT * FROM 't_funcionario' WHERE cpf = ?", (cpf,))
        linha = cursor.fetchone()
        funcionario = self._linha_para_funcionario(linha)

        conexao_db.close()	
        return funcionario
    
    @staticmethod
    def _linha_para_funcionario(row):
        if row:                
            db_data_nasc = date.fromisoformat(row[4]) 
            db_ativo = bool(row[7])                
                
            funcionario_obj = Funcionario(
                cpf=row[0],
                nome=row[1],
                senha=row[2],
                email=row[3],
                data_nascimento=db_data_nasc,
                salario=row[5],
                tipo=row[6],
                ativo=db_ativo,
                id_supervisor=row[8],
                motivo_demissao=row[9]
            )
            return funcionario_obj
        return None
    
    def demitir(self, cpf_gerente: str, cpf_funcionario: str):
        pass