from sqlite3 import Connection
from database.connection import DatabaseConnection
from classes.custom_exception import CustomException
from classes.pedido import Pedido
from services.pedido_service import PedidoService

class PedidoServiceImpl(PedidoService):
    def __init__(self, banco_de_dados: DatabaseConnection):
        self.__banco_de_dados = banco_de_dados

    def adicionar_pedido(self, id_responsavel: str, estado:int, lista_produtos: list[list[int]]):
        try:
            conexao_db = self.__banco_de_dados.get_connection()
            if not conexao_db:
                raise CustomException("Erro ao conectar com o banco de dados")

            cursor = conexao_db.cursor()
            cursor.execute("INSERT INTO t_pedido (id_responsavel, estado) VALUES (?,?)", (id_responsavel,estado,))

            id_pedido = cursor.lastrowid
            if not id_pedido:
                raise CustomException("Erro ao buscar id do pedido criado")

            dados_para_inserir = []
            for id_produto, quantidade_produto in lista_produtos:
                dados_para_inserir.append((id_produto, id_pedido, quantidade_produto))

            cursor.executemany(
                    "INSERT INTO t_pedido_produto (id_produto, id_pedido, quantidade) VALUES (?, ?, ?)", 
                    dados_para_inserir
                )
            
            conexao_db.commit()
            return self.buscar_pedido(id_pedido)
        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Erro ao cadastrar pedido: {e}")
            raise CustomException("Erro ao cadastrar pedido")
        finally:
            if conexao_db:
                conexao_db.close()

    def editar_pedido(self,id:int, estado:int):
        try:
            conexao_db = self.__banco_de_dados.get_connection()
            if not conexao_db:
                raise CustomException("Erro ao conectar com o banco de dados")
                    
            cursor = conexao_db.cursor()
            cursor.execute("UPDATE t_pedido SET estado = ? WHERE id = ?",(estado,id,))
            conexao_db.commit()                
            
            return self.buscar_pedido(id)
        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Erro ao editar pedido: {e}")
            raise CustomException("Erro ao editar pedido")
        finally:
            if conexao_db:
                conexao_db.close()

    def remover_pedido(self,id:int):
        conexao_db = self.__banco_de_dados.get_connection()
        if not conexao_db:
            raise CustomException("Erro ao conectar com o banco de dados")
        
        try:
            pedido = self.buscar_pedido(id)
            
            cursor = conexao_db.cursor()
            cursor.execute("DELETE FROM t_pedido WHERE id =?",(id,))
            cursor.execute("DELETE FROM t_pedido_produto WHERE id_pedido =?",(id,))
            conexao_db.commit()

            return pedido
        except CustomException as e:
            raise CustomException("Pedido não encontrado")
        except Exception as e:
            print(f"Erro ao remover pedido: {e}")
            raise CustomException("Erro ao remover pedido")
        finally:
            if conexao_db:
                conexao_db.close()

    def buscar_pedido(self, id:int):
        try:
            conexao_db = self.__banco_de_dados.get_connection()
            if not conexao_db:
                raise CustomException("Erro ao conectar com o banco de dados")
        
            cursor = conexao_db.cursor()
            cursor.execute("SELECT * FROM t_pedido WHERE id = ?",(id,))
            result = cursor.fetchone()
            pedido = Pedido(
                id=result['id'],
                id_responsavel=result['id_responsavel'],
                estado=result['estado'],
                produtos=[]
            )
            
            cursor.execute("SELECT * FROM t_pedido_produto WHERE id_pedido = ?", (id,))
            result = cursor.fetchall()
            
            pedido.lista_produtos = []
            for produto in result:                
                pedido.lista_produtos.append((produto['id_produto'], produto['quantidade']))
                            
            return pedido
        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Erro ao buscar pedido: {e}")
            raise CustomException("Erro ao buscar pedido")
        finally:
            if conexao_db:
                conexao_db.close()