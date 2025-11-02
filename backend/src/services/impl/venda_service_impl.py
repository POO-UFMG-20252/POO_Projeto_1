from sqlite3 import Connection

from database.connection import DatabaseConnection
from services.venda_service import VendaService
from datetime import datetime

class VendaSeriviceImpl(VendaService):
    def __init__(self, banco_de_dados: DatabaseConnection):
        self.banco_de_dados = banco_de_dados

    def registrar_venda(self,id_responsavel:int, lista_venda: list[list[int]], id_mercado:int):
        conexao_db = self.banco_de_dados.get_connection()
        cursor = conexao_db.cursor()
        try:
            #verificação de quantia de produto no estoque do mercado
            for id_produto, quantidade in lista_venda:
                cursor.execute("SELECT quantidade FROM t_estoque_mercado WHERE id_mercado = ? AND id_produto = ?", (id_mercado,id_produto,))
                registro = cursor.fetchone
                if not registro:
                    print(f"{id_produto} não encontrad0 no estoque do mercado {id_mercado}",)
                    conexao_db.close()
                    return False
                quantidade_estoque = registro[0]
                if quantidade_estoque < quantidade:
                    print("produto {id_produto} sem estoque;({quantidade_estoque}disponível e {quantidade} requisitada")
                    conexao_db.close()
                    return False
            #inserção em tabela t_vendas
            #garantir que cada id seja maior que o anterior
            cursor.execute("SELECT MAX(id) FROM t_vendas")
            id_anterior = cursor.fetchone()[0]
            id_proximo = (id_anterior+1) if id_anterior else 1

            data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute("INSERT INTO t_vendas (id,id_responsavel,time) VALUES(?,?,?)", (id_proximo, id_responsavel,data_hora))

            #inserção de cada produto no t_vendas_produto

            for id_produto,quantidade in lista_venda:
                cursor.execute("INSERT INTO t_vendas_produtos (id_venda, id_produto,quantidade)VALUES(?,?,?,)", (id_proximo, id_produto,quantidade))
                cursor.execute("UPDATE t_estoque_mercado SET quantidade = quantidade - ? WHERE id_mercado = ? AND id_produto =?", (quantidade, id_mercado, id_produto))
            conexao_db.commit()
            #possível print de sucesso
            return True
        except:
            print(f"erro no registro de venda")
            return False
        finally:
            conexao_db.close()
            