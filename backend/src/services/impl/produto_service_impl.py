import sqlite3
from database.connection import DatabaseConnection
from classes.produto import Produto
from services.produto_service import ProdutoService

class ProdutoServiceImpl(ProdutoService):
    def __init__(self, banco_de_dados: DatabaseConnection):
        self.banco_de_dados = banco_de_dados

    @staticmethod
    def adicionar_produto(self,id: int, nome: str, marca: str):
        conexao_db = self.banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        cursor.execute("INSERT INTO t_produto (id,nome,marca) VALUES (?, ?,?)", (id,nome,marca,))
        conexao_db.close()
    
    @staticmethod
    def remover_produto(self,id: int):
        conexao_db = self.banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        cursor.execute("DELETE FROM t_produto WHERE id =?",(id,))
        conexao_db.close()

    @staticmethod
    def editar_produto(self,id: int, nome:str, marca:str):
        conexao_db = self.banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        cursor.execute("UPDATE t_produto SET nome = ? marca = ? WHERE id = ?",(nome,marca,id),)
        conexao_db.close()

    @staticmethod
    def busca_geral_produto(self):
        produtos = [] #array final/geral

        conexao_db = self.banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        cursor.execute("SELECT id,nome,marca FROM t_produto ")
        results = cursor.fetchall()#pega todos os produtos
        for result in results:
            produto = Produto(*result)
            produtos.append(produto)#pega cada item do fetchall e salva como um objeto na lista produtos
        return produtos
        conexao_db.close()
    
    @staticmethod
    def busca_produto(self, id: int):
        conexao_db = self.banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        cursor.execute("SELECT id,nome,marca FROM t_produto WHERE id =?",(id,))
        result = cursor.fetchone()
        return result