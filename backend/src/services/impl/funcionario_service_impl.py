import bcrypt
import sqlite3
from typing import List
from datetime import datetime

from classes.funcionario import Funcionario
from classes.custom_exception import CustomException
from database.connection import DatabaseConnection
from services.funcionario_service import FuncionarioService
from services.impl.autenticacao_service_impl import AutenticacaoServiceImpl

class FuncionarioServiceImpl(FuncionarioService):
    def __init__(self, database_connection: DatabaseConnection):
        self.__banco_de_dados = database_connection
    
    def listar_funcionarios(self) -> List[Funcionario]:
        conexao = self.__banco_de_dados.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")

        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT cpf, nome, data_admissao, tipo, ativo, salario
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
                    salario=float(resultado['salario']),
                    tipo=resultado['tipo'],
                    ativo=bool(resultado['ativo'])
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
        conexao = self.__banco_de_dados.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")
            
        try:
            cursor = conexao.cursor()
            cursor.execute("""
                SELECT cpf, nome, email, senha, data_nascimento, 
                    salario, tipo, ativo, data_admissao
                FROM t_funcionario 
                WHERE REPLACE(REPLACE(REPLACE(cpf, '.', ''), '-', ''), ' ', '') = ?  AND ativo = 1
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
                data_admissao=resultado['data_admissao']
            )
            
        except Exception as e:
            print(f"Erro ao buscar funcionário: {e}")
            raise CustomException("Erro ao buscar funcionário")
        finally:
            if conexao:
                conexao.close()
    
    def demitir(self, cpf_funcionario: str, motivo: str):      
        conexao = None
        try:            
            conexao = self.__banco_de_dados.get_connection()
            if not conexao:
                raise CustomException("Erro ao conectar com o banco de dados")
            
            cursor = conexao.cursor()
            
            # Usar transação explícita
            cursor.execute("BEGIN TRANSACTION")
            
            try:
                # Primeiro verificar se o funcionário existe e está ativo
                cursor.execute("""
                    SELECT * FROM t_funcionario 
                    WHERE REPLACE(REPLACE(REPLACE(cpf, '.', ''), '-', ''), ' ', '') = ? 
                """, (cpf_funcionario,))
                
                resultado = cursor.fetchone()
                
                if not resultado:
                    raise CustomException("Funcionário não encontrado")
                    
                if not resultado['ativo']:
                    raise CustomException("Funcionário já foi demitido")
                
                # Fazer a atualização
                cursor.execute("""
                    UPDATE t_funcionario 
                    SET ativo = 0, motivo_demissao = ? 
                    WHERE REPLACE(REPLACE(REPLACE(cpf, '.', ''), '-', ''), ' ', '') = ?
                """, (motivo, cpf_funcionario))
                
                # Commit da transação
                cursor.execute("COMMIT")
                
            except Exception as e:
                # Rollback em caso de erro
                cursor.execute("ROLLBACK")
                raise e
            
            # Buscar os dados atualizados (fora da transação)
            cursor.execute("""
                SELECT * FROM t_funcionario 
                WHERE REPLACE(REPLACE(REPLACE(cpf, '.', ''), '-', ''), ' ', '') = ?
            """, (cpf_funcionario,))
            
            resultado = cursor.fetchone()
            
            return {
                'cpf': resultado['cpf'],
                'nome': resultado['nome'],
                'data_admissao': resultado['data_admissao'],
                'tipo': resultado['tipo'],
                'ativo': resultado['ativo']
            }
            
        except CustomException as e:
            raise e
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                raise CustomException("Sistema ocupado. Tente novamente em alguns segundos.")
            else:
                print(f"Erro de banco de dados ao demitir usuário: {e}")
                raise CustomException("Erro de banco de dados ao demitir funcionário")
        except Exception as e:
            print(f"Erro inesperado ao demitir usuário: {e}")
            raise CustomException("Erro inesperado ao demitir funcionário")
        finally:
            if conexao:
                conexao.close()
    
    
    def cadastrar_funcionario(self, nome: str, cpf: str, email: str, senha: str, data_nascimento: str, salario: float, tipo: str) -> Funcionario:
        conexao = self.__banco_de_dados.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")

        try:
            cursor = conexao.cursor()
            
            cpf = cpf.replace('.', '')
            cpf = cpf.replace('-', '')
            cpf = cpf.replace(' ', '')
        
            self._validar_cpf(cursor, cpf)
            self._validar_email(cursor, email)

            # Mapear tipo string para número
            tipo_map = {
                'Gerente': 0,
                'Repositor': 1,
                'Caixa': 2
            }

            tipo_numero = tipo_map.get(tipo)
            if tipo_numero is None:
                raise CustomException("Tipo de funcionário inválido")

            senha_hash = AutenticacaoServiceImpl.gerar_hash_senha(senha)
            
            cursor.execute("""
                INSERT INTO t_funcionario (
                    cpf, nome, senha, email, data_nascimento, data_admissao, 
                    salario, tipo, ativo
                ) VALUES (?, ?, ?, ?, ?, date('now'), ?, ?, 1)
            """, (cpf, nome, senha_hash, email, data_nascimento, float(salario), tipo_numero))

            conexao.commit()

            # Buscar o funcionário recém-criado para retornar
            cursor.execute("""
                SELECT cpf, nome, email, data_nascimento, data_admissao, 
                    salario, tipo, ativo
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
        
    def bater_ponto(self, cpf_funcionario: str, tipo: int) -> dict:

        conexao = self.__banco_de_dados.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")

        try:
            cursor = conexao.cursor()

            # Limpar CPF
            cpf_limpo = cpf_funcionario.replace('.', '').replace('-', '').replace(' ', '')
            print(f"Buscando funcionário com CPF: {cpf_limpo}")

            # Verificar se funcionário existe e está ativo
            cursor.execute("""
                SELECT cpf, nome, ativo FROM t_funcionario 
                WHERE REPLACE(REPLACE(REPLACE(cpf, '.', ''), '-', ''), ' ', '') = ?
            """, (cpf_limpo,))

            funcionario = cursor.fetchone()

            if not funcionario:
                raise CustomException("Funcionário não encontrado")

            if not funcionario['ativo']:
                raise CustomException("Funcionário demitido não pode bater ponto")

            print(f"Funcionário encontrado: {funcionario['nome']}")

            # Verificar se já existe um ponto do mesmo tipo no mesmo dia
            data_hoje = datetime.now().strftime('%Y-%m-%d')

            cursor.execute("""
                SELECT id FROM t_ponto 
                WHERE id_usuario = ? 
                AND DATE(horario) = ?
                AND tipo = ?
            """, (cpf_limpo, data_hoje, tipo))

            ponto_existente = cursor.fetchone()

            if ponto_existente:
                tipo_texto = "entrada" if tipo == 0 else "saída"
                raise CustomException(f"Ponto de {tipo_texto} já registrado hoje")

            # Inserir o ponto
            data_hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"Registrando ponto: {data_hora_atual}, tipo: {tipo}")

            cursor.execute("""
                INSERT INTO t_ponto (id_usuario, horario, tipo)
                VALUES (?, ?, ?)
            """, (cpf_limpo, data_hora_atual, tipo))

            conexao.commit()
            print("Ponto inserido no banco")

            # Buscar dados do ponto registrado
            cursor.execute("""
                SELECT p.id, p.id_usuario, p.horario, p.tipo, f.nome
                FROM t_ponto p
                JOIN t_funcionario f ON p.id_usuario = f.cpf
                WHERE p.id = last_insert_rowid()
            """)

            ponto = cursor.fetchone()

            return {
                'id': ponto['id'],
                'id_usuario': ponto['id_usuario'],
                'nome': ponto['nome'],
                'horario': ponto['horario'],
                'tipo': ponto['tipo'],
                'tipo_descricao': 'Entrada' if ponto['tipo'] == 0 else 'Saída',
                'mensagem': f"Ponto de {'entrada' if ponto['tipo'] == 0 else 'saída'} registrado com sucesso"
            }

        except CustomException as e:
            print(f"CustomException no serviço: {e}")
            raise e
        except Exception as e:
            print(f"Erro inesperado ao bater ponto no serviço: {e}")
            import traceback
            traceback.print_exc()
            raise CustomException("Erro ao registrar ponto")
        finally:
            if conexao:
                conexao.close()