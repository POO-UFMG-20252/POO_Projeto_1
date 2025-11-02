import bcrypt
import sqlite3
from typing import List

from classes.funcionario import Funcionario
from classes.custom_exception import CustomException
from database.connection import DatabaseConnection
from services.funcionario_service import FuncionarioService
from services.autenticacao_service import AutenticacaoService

class FuncionarioServiceImpl(FuncionarioService):
    def __init__(self, database_connection: DatabaseConnection):
        self.db_connection = database_connection
    
    def listar_funcionarios(self) -> List[Funcionario]:
        conexao = self.db_connection.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")
            
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT cpf, nome, data_admissao 
                FROM t_funcionario 
                WHERE ativo = 1
                ORDER BY nome
            """)
            
            resultados = cursor.fetchall()
            funcionarios = []
            
            for resultado in resultados:
                # Criar funcionário com valores padrão para campos não buscados
                funcionario = Funcionario(
                    cpf=resultado['cpf'],
                    nome=resultado['nome'],
                    data_admissao=resultado['data_admissao'],
                    email="",  # valor padrão
                    senha="",  # valor padrão  
                    data_nascimento="",  # valor padrão
                    salario=0,  # valor padrão
                    tipo=0,  # valor padrão
                    ativo=True,  # valor padrão
                    id_supervisor=0  # valor padrão
                )
                funcionarios.append(funcionario)
                
            return funcionarios
            
        except Exception as e:
            print(f"Erro ao buscar funcionários: {e}")
            raise CustomException("Erro ao buscar lista de funcionários")
        finally:
            if conexao:
                conexao.close()
    
    def buscar_funcionario(self, cpf: str) -> Funcionario:
        conexao = self.db_connection.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")
            
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT cpf, nome, email, senha, data_nascimento, 
                    salario, tipo, ativo, id_supervisor, data_admissao
                FROM t_funcionario 
                WHERE cpf = ? AND ativo = 1
            """, (cpf,))
            
            resultado = cursor.fetchone()
            
            if not resultado:
                return None
                
            return Funcionario(
                cpf=resultado['cpf'],
                nome=resultado['nome'],
                email=resultado['email'],
                senha=resultado['senha'],
                data_nascimento=resultado['data_nascimento'],
                salario=resultado['salario'],
                tipo=resultado['tipo'],
                ativo=bool(resultado['ativo']),
                id_supervisor=resultado['id_supervisor'],
                data_admissao=resultado['data_admissao']
            )
            
        except Exception as e:
            print(f"Erro ao buscar funcionário: {e}")
            raise CustomException("Erro ao buscar funcionário")
        finally:
            if conexao:
                conexao.close()
    
    def demitir(self, cpf_gerente: str, cpf_funcionario: str):
        pass
    
    def cadastrar_funcionario(self, nome: str, cpf: str, senha: str, email: str, data_nascimento: str, salario: float, tipo: int) -> Funcionario:
        conexao = self.db_connection.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")
        
        try:
            cursor = conexao.cursor()
        
            self._validar_cpf(cursor, cpf)
            self._validar_email(cursor, email)

            # Mapear tipo string para número
            tipo_map = {
                'Gerente': 0,
                'Caixa': 1,
                'Repositor': 2
            }

            tipo_numero = tipo_map.get(tipo)
            if tipo_numero is None:
                raise CustomException("Tipo de funcionário inválido")

            # Inserir novo funcionário
            # Senha padrão: "123456" (hash bcrypt)
            senha_hash = AutenticacaoService.gerar_hash_senha(senha)

            cursor.execute("""
                INSERT INTO t_funcionario (
                    cpf, nome, senha, email, data_nascimento, data_admissao, 
                    salario, tipo, ativo, id_supervisor
                ) VALUES (?, ?, ?, ?, ?, date('now'), ?, ?, 1, 0)
            """, (cpf, nome, senha_hash, email, data_nascimento, float(salario), tipo_numero))

            conexao.commit()

            # Buscar o funcionário recém-criado para retornar
            cursor.execute("""
                SELECT cpf, nome, email, data_nascimento, data_admissao, 
                    salario, tipo, ativo, id_supervisor
                FROM t_funcionario 
                WHERE cpf = ?
            """, (cpf,))

            resultado = cursor.fetchone()

            if not resultado:
                raise CustomException("Erro ao recuperar funcionário cadastrado")

            return Funcionario(
                cpf=resultado['cpf'],
                nome=resultado['nome'],
                email=resultado['email'],
                senha="",
                data_nascimento=resultado['data_nascimento'],
                salario=resultado['salario'],
                tipo=resultado['tipo'],
                ativo=bool(resultado['ativo']),
                id_supervisor=resultado['id_supervisor'],
                data_admissao=resultado['data_admissao']
            )
        
        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Erro ao cadastrar funcionário: {e}")
            raise CustomException("Erro ao cadastrar funcionário")
        finally:
            if conexao:
                conexao.close()
                
    def _validar_cpf(self, cursor: sqlite3.Cursor, cpf: str):
        if (len(cpf) != 11) :
            raise CustomException("CPF invalido")
        
        # Verificar se CPF já existe
        cursor.execute("SELECT cpf FROM t_funcionario WHERE cpf = ?", (cpf,))
        if cursor.fetchone():
            raise CustomException("CPF já cadastrado")
        
    def _validar_email(self, cursor: sqlite3.Cursor, email: str):
        if (email.find("@") == -1):
            raise CustomException("Email inválido")
        
        if (email.split("@")[1].find(".") == -1):
            raise CustomException("Email inválido")
        
        # Verificar se email já existe
        cursor.execute("SELECT cpf FROM t_funcionario WHERE email = ?", (email,))
        if cursor.fetchone():
            raise CustomException("Email já cadastrado")