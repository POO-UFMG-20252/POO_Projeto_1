from sqlite3 import Connection
from database.connection import DatabaseConnection
from classes.custom_exception import CustomException
from classes.pedido import Pedido
from services.pedido_service import PedidoService

class PedidoServiceImpl(PedidoService):
    def __init__(self, banco_de_dados: DatabaseConnection):
        self.__banco_de_dados = banco_de_dados

    def adicionar_pedido(self,id: int, id_responsavel:int,id_mercado:int,estado:int):
        conexao_db = self.__banco_de_dados.get_connection()
        if not conexao_db:
            raise CustomException("Erro ao conectar com o banco de dados")

        cursor = conexao_db.cursor()
        cursor.execute("INSERT INTO t_pedido (id,id_responsavel,id_mercado) VALUES (?,?,?,?)", (id,id_responsavel,id_mercado,estado,))
        conexao_db.commit()
        conexao_db.close()

    def editar_pedido(self,id:int, estado:int):
        conexao_db = self.__banco_de_dados.get_connection()
        if not conexao_db:
            raise CustomException("Erro ao conectar com o banco de dados")
        
        cursor = conexao_db.cursor()
        cursor.execute("UPDATE t_pedido SET estado = ? WHERE id = ?",(estado,id,))
        conexao_db.commit()
        
        cursor.execute("SELECT * FROM t_pedido WHERE id = ?",(id,))
        result = cursor.fetchone()
        pedido = Pedido(*result)
        
        conexao_db.close()
        
        return pedido

    def remover_pedido(self,id:int):
        conexao_db = self.__banco_de_dados.get_connection()
        if not conexao_db:
            raise CustomException("Erro ao conectar com o banco de dados")

        cursor = conexao_db.cursor()
        cursor.execute("SELECT * FROM t_pedido WHERE id = ?",(id,))
        result = cursor.fetchone()
        pedido = Pedido(*result)
        
        cursor.execute("DELETE FROM t_produto WHERE id =?",(id,))
        conexao_db.commit()
        conexao_db.close()
        
        return pedido

    def buscar_pedido(self, id:int):
        conexao_db = self.__banco_de_dados.get_connection()
        if not conexao_db:
            raise CustomException("Erro ao conectar com o banco de dados")
        
        cursor = conexao_db.cursor()
        cursor.execute("SELECT * FROM t_pedido WHERE id = ?",(id,))
        result = cursor.fetchone()
        conexao_db.close()
        
        return Pedido(*result)