import sqlite3
from database.connection import DatabaseConnection
from classes.produto import Produto
from services.produto_service import ProdutoService

class ProdutoServiceImpl(ProdutoService):
    def __init__(self, banco_de_dados: DatabaseConnection):
        self.banco_de_dados = banco_de_dados

    @staticmethod
    def adicionar_produto(self,id: int, nome: str, marca: str):
        with sqlite3.connect(self.banco_de_dados) as con:
            cur = con.cursor()
            cur.execute("INSERT INTO t_produto (id,nome,marca) VALUES (?, ?,?)", (id,nome,marca,))
            con.commit()
    
    @staticmethod
    def remover_produto(self,id: int):
        with sqlite3.connect(self.banco_de_dados) as con:
            cur = con.cursor()
            cur.execute("DELETE FROM t_produto WHERE id =?",(id,))

    @staticmethod
    def editar_produto(self,id: int, nome:str, marca:str):
        with sqlite3.connect(self.banco_de_dados) as con:
            cur = con.cursor()
            cur.execute("UPDATE t_produto SET nome = ? marca = ? WHERE id = ?",(nome,marca,id),)

    @staticmethod
    def busca_geral_produto(self):
        produtos = [] #array final/geral
        try:
            with sqlite3.connect(self.banco_de_dados) as con:
                cur = con.cursor()
                cur.execute("SELECT id,nome,marca FROM t_produto ")
                results = cur.fetchall()#pega todos os produtos
                for result in results:
                    produto = Produto(*result)
                    produtos.append(produto)#pega cada item do fetchall e salva como um objeto na lista produtos
            return produtos
        except:
            return []#retorna lista vazia caso de erro
    
    @staticmethod
    def busca_produto(self, id: int):
        try:
            with sqlite3.connect(self.banco_de_dados) as con:
                cur = con.cursor()
                cur.execute("SELECT id,nome,marca FROM t_produto WHERE id =?",(id,))
                result = cur.fetchone()
                return result
        except:
            return None