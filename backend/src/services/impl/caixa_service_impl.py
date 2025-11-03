from services.caixa_service import CaixaService
from classes.produto import Produto
from classes.custom_exception import CustomException
from database.connection import DatabaseConnection
from typing import List, Dict, Any
from datetime import datetime
import random
import string

class CaixaServiceImpl(CaixaService):
    def __init__(self, database_connection: DatabaseConnection):
        self.__banco_de_dados = database_connection
    
    def obter_produto_por_id(self, id_produto: int) -> Produto:
        conexao = self.__banco_de_dados.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")
            
        try:
            cursor = conexao.cursor()
            
            cursor.execute("""
                SELECT id, nome, marca, preco 
                FROM t_produto 
                WHERE id = ?
            """, (id_produto,))
            
            resultado = cursor.fetchone()
            
            if not resultado:
                raise CustomException("Produto não encontrado")
            
            return Produto(
                id=resultado['id'],
                nome=resultado['nome'],
                marca=resultado['marca'],
                preco=resultado['preco'] or 0.0
            )
            
        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Erro ao buscar produto: {e}")
            raise CustomException("Erro ao buscar produto")
        finally:
            if conexao:
                conexao.close()
    
    def _gerar_codigo_pix(self):
        """Gera um código PIX aleatório"""
        caracteres = string.ascii_uppercase + string.digits
        return 'PIX' + ''.join(random.choices(caracteres, k=10))
    
    def processar_venda(self, itens_venda: List[Dict[str, Any]], id_operador: int) -> Dict[str, Any]:
        conexao = self.__banco_de_dados.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")
            
        try:
            cursor = conexao.cursor()
            
            # Calcular total da venda
            total_venda = sum(item['preco'] * item['quantidade'] for item in itens_venda)
            
            # Gerar código PIX
            codigo_pix = self._gerar_codigo_pix()
            
            # Processar cada item da venda
            for item in itens_venda:
                id_produto = item['id']
                quantidade_vendida = item['quantidade']
                total_item = item['preco'] * item['quantidade']
                
                # Buscar itens em estoque ordenados por local (loja primeiro, depois armazém)
                cursor.execute("""
                    SELECT id, quantidade, local 
                    FROM t_estoque_armazem 
                    WHERE id_produto = ? AND quantidade > 0
                    ORDER BY local DESC, id ASC
                """, (id_produto,))
                
                itens_estoque = cursor.fetchall()
                
                if not itens_estoque:
                    raise CustomException(f"Produto '{item['nome']}' não encontrado em estoque")
                                
                # Calcular estoque total disponível
                estoque_total = sum(item['quantidade'] for item in itens_estoque)
                if estoque_total < quantidade_vendida:
                    raise CustomException(f"Estoque insuficiente para '{item['nome']}'. Disponível: {estoque_total}, Solicitado: {quantidade_vendida}")
                
                # Remover do estoque na ordem: loja primeiro, depois armazém
                quantidade_restante = quantidade_vendida
                
                for item_estoque in itens_estoque:
                    if quantidade_restante <= 0:
                        break
                    
                    id_item_estoque = item_estoque['id']
                    quantidade_disponivel = item_estoque['quantidade']
                    local = item_estoque['local']
                    
                    quantidade_a_remover = min(quantidade_restante, quantidade_disponivel)
                                        
                    # Atualizar estoque
                    nova_quantidade = quantidade_disponivel - quantidade_a_remover
                    
                    if nova_quantidade == 0:
                        # Se zerou o estoque, remove o item
                        cursor.execute("DELETE FROM t_estoque_armazem WHERE id = ?", (id_item_estoque,))
                        print(f"Item {id_item_estoque} removido do estoque (quantidade zerada)")
                    else:
                        # Atualiza a quantidade
                        cursor.execute("UPDATE t_estoque_armazem SET quantidade = ? WHERE id = ?", 
                                     (nova_quantidade, id_item_estoque))
                        print(f"Item {id_item_estoque} atualizado: {quantidade_disponivel} → {nova_quantidade}")
                    
                    quantidade_restante -= quantidade_a_remover
                
                # Inserir na tabela t_vendas
                cursor.execute("""
                    INSERT INTO t_vendas (id_produto, quantidade, total, codigo_pix)
                    VALUES (?, ?, ?, ?)
                """, (id_produto, quantidade_vendida, total_item, codigo_pix))
                
                print(f"Venda registrada para produto {id_produto}: {quantidade_vendida} unidades")
            
            conexao.commit()
            
            return {
                'id_venda': cursor.lastrowid,
                'total_venda': total_venda,
                'codigo_pix': codigo_pix,
                'quantidade_itens': len(itens_venda),
                'data_hora': datetime.now().isoformat(),
                'mensagem': 'Venda processada com sucesso'
            }
            
        except CustomException as e:
            conexao.rollback()
            raise e
        except Exception as e:
            conexao.rollback()
            print(f"Erro ao processar venda: {e}")
            raise CustomException("Erro ao processar venda")
        finally:
            if conexao:
                conexao.close()