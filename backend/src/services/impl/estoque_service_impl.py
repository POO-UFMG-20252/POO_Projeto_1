from abc import abstractmethod
from typing import List

from classes.estoque import Estoque
from classes.custom_exception import CustomException
from database.connection import DatabaseConnection
from services.estoque_service import EstoqueService

class EstoqueServiceImpl(EstoqueService):
    def __init__(self, database_connection: DatabaseConnection):
        self.database_connection = database_connection
    
    def buscar_todos_itens(self) -> List[Estoque]:
        conn = self.database_connection.get_connection()
        if conn is None:
            raise CustomException("Conexão com banco falhou!")
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estoque")
            rows = cursor.fetchall()
            print(f"Número de registros no banco: {len(rows)}")
            
            itens = []
            for row in rows:
                item = Estoque(
                    id=row['id'],
                    nome=row['nome'],
                    quantidade=row['quantidade'],
                    localizacao=row['localizacao'],
                    linha=row['linha'],
                    coluna=row['coluna']
                )
                itens.append(item.to_dict())
            
            print(f"Itens convertidos: {len(itens)}")
            return itens
        except Exception as e:
            print(f"Erro ao buscar itens: {e}")
            raise CustomException("Erro inesperado ao buscar itens do estoque!")
        finally:
            conn.close()
        
    def buscar_produto_por_id(self, id: str) -> Estoque:
        conn = self.database_connection.get_connection()
        if conn is None:
            raise CustomException("Conexão com banco falhou!")
        
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM estoque WHERE id = {id}")
            row = cursor.fetchone()
            if row:
                return Estoque(
                    id=row['id'],
                    nome=row['nome'],
                    quantidade=row['quantidade'],
                    localizacao=row['localizacao'],
                    linha=row['linha'],
                    coluna=row['coluna']
                )
            
        except Exception as e:
            print(f"Erro ao buscar item com id {id}: {e}")
            raise CustomException("Erro inesperado ao buscar item no estoque!")
        finally:
            conn.close()