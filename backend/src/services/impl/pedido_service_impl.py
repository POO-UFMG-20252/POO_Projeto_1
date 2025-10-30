from sqlite3 import Connection
from database.connection import DatabaseConnection
from classes.pedido import Pedido
from services.pedido_service import PedidoService

class PedidoServiceImpl(PedidoService):
    def __init__(self, banco_de_dados: DatabaseConnection):
        self.banco_de_dados = banco_de_dados

    @staticmethod
    def adicionar_pedido(self,id: int, id_responsavel:int,id_mercado:int,estado:int):
        conexao_db = self.banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        cursor.execute("INSERT INTO t_pedido (id,id_responsavel,id_mercado) VALUES (?,?,?,?)", (id,id_responsavel,id_mercado,estado,))
        conexao_db.commit()
        conexao_db.close()

    @staticmethod
    def editar_pedido(self,id:int, estado:str):
        conexao_db = self.banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        cursor.execute("UPDATE t_pedido SET estado = ? WHERE id = ?",(estado,id,))
        conexao_db.commit()
        conexao_db.close()

    @staticmethod
    def remover_pedido(self,id:int):
        conexao_db = self.banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        cursor.execute("DELETE FROM t_produto WHERE id =?",(id,))
        conexao_db.commit()
        conexao_db.close()