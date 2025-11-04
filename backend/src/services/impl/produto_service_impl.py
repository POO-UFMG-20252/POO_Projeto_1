import sqlite3
from database.connection import DatabaseConnection
from classes.produto import Produto
from classes.custom_exception import CustomException
from services.produto_service import ProdutoService

class ProdutoServiceImpl(ProdutoService):
    def __init__(self, banco_de_dados: DatabaseConnection):
        self.__banco_de_dados = banco_de_dados

    def adicionar_produto(self, nome: str, marca: str, preco: float):
        conexao_db = self.__banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        
        cursor.execute("INSERT INTO t_produto (nome,marca,preco) VALUES (?,?,?)", (nome,marca,preco))
        conexao_db.commit()
        
        id = cursor.lastrowid
        
        cursor.execute("SELECT * FROM t_produto WHERE id = ?", (id,))
        produto = cursor.fetchone()
        conexao_db.close()
        return Produto.from_dict(produto)
    
    def remover_produto(self,id: int):
        conexao_db = self.__banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        
        cursor.execute("SELECT * FROM t_produto WHERE id = ?",(id,))
        produto_preexistente = cursor.fetchone()
        
        if not produto_preexistente:
            raise CustomException("Produto não encontrado")
                
        cursor.execute("DELETE FROM t_produto WHERE id =?",(id,))
        conexao_db.commit()
        conexao_db.close()
        
        return Produto.from_dict(produto_preexistente)

    def editar_produto(self,id: int, nome:str, marca:str, preco: float):
        conexao_db = self.__banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        cursor.execute("UPDATE t_produto SET nome = ?, marca = ?, preco = ? WHERE id = ?",(nome,marca, preco,id))
        conexao_db.commit()
        
        cursor.execute("SELECT * FROM t_produto WHERE id =?",(id,))
        produto = cursor.fetchone()
        
        conexao_db.close()
        
        return Produto.from_dict(produto)

    def busca_geral_produto(self):
        produtos = [] #array final/geral

        conexao_db = self.__banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        cursor.execute("SELECT * FROM t_produto")
        results = cursor.fetchall()#pega todos os produtos
        for result in results:
            produto = Produto.from_dict(result).to_dict()
            produtos.append(produto)#pega cada item do fetchall e salva como um objeto na lista produtos
        conexao_db.close()
        return produtos
    
    def busca_produto(self, id: int):
        conexao_db = self.__banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        cursor.execute("SELECT * FROM t_produto WHERE id =?",(id,))
        result = cursor.fetchone()
        return Produto.from_dict(result)
    
    def buscar_produtos_por_nome(self, termo: str):
        conexao = self.__banco_de_dados.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")
            
        try:
            cursor = conexao.cursor()
            
            # Buscar produtos que contenham o termo no nome OU na marca (case insensitive)
            cursor.execute("""
                SELECT id, nome, marca, preco 
                FROM t_produto 
                WHERE LOWER(nome) LIKE LOWER(?) OR LOWER(marca) LIKE LOWER(?)
                LIMIT 10
            """, (f'%{termo}%', f'%{termo}%'))
            
            resultados = cursor.fetchall()
            produtos = []
            
            for resultado in resultados:
                produto = Produto(
                    id=resultado['id'],
                    nome=resultado['nome'],
                    marca=resultado['marca'],
                    preco=resultado['preco'] or 0.0
                )
                produtos.append(produto)
                
            return produtos
            
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
            raise CustomException("Erro ao buscar produtos")
        finally:
            if conexao:
                conexao.close()
