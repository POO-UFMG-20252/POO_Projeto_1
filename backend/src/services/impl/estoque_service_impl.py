from services.estoque_service import EstoqueService
from classes.produto import Produto
from classes.estoque import ItemEstoque
from classes.custom_exception import CustomException
from database.connection import DatabaseConnection
from typing import List, Dict, Any

class EstoqueServiceImpl(EstoqueService):
    def __init__(self, database_connection: DatabaseConnection):
        self.__banco_de_dados = database_connection
    
    def listar_produtos(self) -> List[Produto]:
        conexao = self.__banco_de_dados.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")
            
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT id, nome, marca FROM t_produto")
            
            resultados = cursor.fetchall()
            produtos = []
            
            for resultado in resultados:
                produto = Produto(
                    id=resultado['id'],
                    nome=resultado['nome'],
                    marca=resultado['marca']
                )
                produtos.append(produto)
                
            return produtos
            
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
            raise CustomException("Erro ao buscar lista de produtos")
        finally:
            if conexao:
                conexao.close()
    
    def listar_estoque_armazem(self, id_mercado: int = 1) -> List[ItemEstoque]:
        return self._listar_estoque_local(0, id_mercado)  # 0 = armazém
    
    def listar_estoque_loja(self, id_mercado: int = 1) -> List[ItemEstoque]:
        return self._listar_estoque_local(1, id_mercado)  # 1 = loja
    
    def _listar_estoque_local(self, local: int, id_mercado: int) -> List[ItemEstoque]:
        conexao = self.__banco_de_dados.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")
            
        try:
            cursor = conexao.cursor()
            
            # Buscar todos os itens do local específico (0=armazém, 1=loja)
            cursor.execute("""
                SELECT ea.id, ea.id_produto, ea.id_mercado, ea.pos_x, ea.pos_y, 
                        ea.quantidade, ea.local, p.nome as produto_nome
                FROM t_estoque_armazem ea
                JOIN t_produto p ON ea.id_produto = p.id
                WHERE ea.id_mercado = ? AND ea.local = ?
            """, (id_mercado, local))
            
            resultados = cursor.fetchall()
            itens_estoque = []
            
            for resultado in resultados:
                # Converter local numérico para string
                local_str = 'armazem' if resultado['local'] == 0 else 'loja'
                
                item = ItemEstoque(
                    id=resultado['id'],
                    id_produto=resultado['id_produto'],
                    id_mercado=resultado['id_mercado'],
                    pos_x=resultado['pos_x'],
                    pos_y=resultado['pos_y'],
                    quantidade=resultado['quantidade'],
                    produto_nome=resultado['produto_nome'],
                    local=local_str
                )
                itens_estoque.append(item)
                
            return itens_estoque
            
        except Exception as e:
            local_str = 'armazem' if local == 0 else 'loja'
            print(f"Erro ao buscar estoque {local_str}: {e}")
            raise CustomException(f"Erro ao buscar estoque {local_str}")
        finally:
            if conexao:
                conexao.close()
    
    def obter_visualizacao_estoque(self, id_mercado: int = 1) -> Dict[str, Any]:
        try:
            # Obter produtos
            produtos = self.listar_produtos()
            
            # Obter estoque do armazém e loja
            estoque_armazem = self.listar_estoque_armazem(id_mercado)
            estoque_loja = self.listar_estoque_loja(id_mercado)
            
            # Configurações das matrizes 
            tamanho_armazem = {'linhas': 5, 'colunas': 5}
            tamanho_loja = {'linhas': 3, 'colunas': 3}
            
            # Criar matrizes vazias
            matriz_armazem = self._criar_matriz_vazia(tamanho_armazem['linhas'], tamanho_armazem['colunas'])
            matriz_loja = self._criar_matriz_vazia(tamanho_loja['linhas'], tamanho_loja['colunas'])
            
            # Preencher matriz do armazém
            for item in estoque_armazem:
                if 0 <= item.pos_x < tamanho_armazem['linhas'] and 0 <= item.pos_y < tamanho_armazem['colunas']:
                    matriz_armazem[item.pos_x][item.pos_y] = {
                        'ocupada': True,
                        'produtoId': item.id_produto,
                        'produto': item.produto_nome,
                        'quantidade': item.quantidade,
                        'porcentagem': min((item.quantidade / 500) * 100, 100),
                        'linha': item.pos_x,
                        'coluna': item.pos_y,
                        'local': 'armazem',
                        'itemId': item.id  # ← IMPORTANTE: incluir o ID do item
                    }
            
            # Preencher matriz da loja
            for item in estoque_loja:
                if 0 <= item.pos_x < tamanho_loja['linhas'] and 0 <= item.pos_y < tamanho_loja['colunas']:
                    matriz_loja[item.pos_x][item.pos_y] = {
                        'ocupada': True,
                        'produtoId': item.id_produto,
                        'produto': item.produto_nome,
                        'quantidade': item.quantidade,
                        'porcentagem': min((item.quantidade / 500) * 100, 100),
                        'linha': item.pos_x,
                        'coluna': item.pos_y,
                        'local': 'loja',
                        'itemId': item.id  # ← IMPORTANTE: incluir o ID do item
                    }
            
            # Lista consolidada de produtos
            produtos_consolidados = []
            for item in estoque_armazem + estoque_loja:
                produtos_consolidados.append({
                    'id': item.id_produto,
                    'nome': item.produto_nome,
                    'quantidade': item.quantidade,
                    'localizacao': item.local,
                    'posicao': {
                        'linha': item.pos_x,
                        'coluna': item.pos_y
                    },
                    'itemId': item.id  # ← IMPORTANTE: incluir o ID do item
                })
            
            return {
                'matrizArmazem': matriz_armazem,
                'matrizLoja': matriz_loja,
                'produtos': produtos_consolidados,
                'tamanhoArmazem': tamanho_armazem,
                'tamanhoLoja': tamanho_loja,
                'capacidadeMaxima': 500
            }
            
        except Exception as e:
            print(f"Erro ao obter visualização do estoque: {e}")
            raise CustomException("Erro ao carregar visualização do estoque")
    
    def _criar_matriz_vazia(self, linhas: int, colunas: int):
        matriz = []
        for i in range(linhas):
            linha = []
            for j in range(colunas):
                linha.append({
                    'ocupada': False,
                    'produtoId': None,
                    'produto': '',
                    'quantidade': 0,
                    'porcentagem': 0,
                    'linha': i,
                    'coluna': j,
                    'local': '',
                    'itemId': None  # ← IMPORTANTE: incluir o ID do item
                })
            matriz.append(linha)
        return matriz
    
    def mover_produto(self, id_item: int, novo_pos_x: int, novo_pos_y: int, novo_local: str) -> bool:
        conexao = self.__banco_de_dados.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")
            
        try:
            cursor = conexao.cursor()
            
            # Buscar o item atual
            cursor.execute("""
                SELECT id_produto, quantidade, local, pos_x, pos_y 
                FROM t_estoque_armazem 
                WHERE id = ?
            """, (id_item,))
            
            resultado = cursor.fetchone()
            if not resultado:
                raise CustomException("Item não encontrado")
            
            id_produto = resultado['id_produto']
            quantidade = resultado['quantidade']
            local_atual = resultado['local']
            
            # Converter novo_local para numérico
            novo_local_num = 0 if novo_local == 'armazem' else 1
            
            # Verificar se a posição de destino está disponível
            if novo_local_num == 0:  # armazém
                cursor.execute("""
                    SELECT id FROM t_estoque_armazem 
                    WHERE id_mercado = 1 AND local = 0 AND pos_x = ? AND pos_y = ? AND id != ?
                """, (novo_pos_x, novo_pos_y, id_item))
                
                if cursor.fetchone():
                    raise CustomException("Posição já ocupada no armazém")
            
            # Atualizar a posição e local do item
            cursor.execute("""
                UPDATE t_estoque_armazem 
                SET pos_x = ?, pos_y = ?, local = ?
                WHERE id = ?
            """, (novo_pos_x, novo_pos_y, novo_local_num, id_item))
            
            conexao.commit()
            return True
            
        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Erro ao mover produto: {e}")
            raise CustomException("Erro ao mover produto")
        finally:
            if conexao:
                conexao.close()
    
    def adicionar_produto(self, id_produto: int, id_mercado: int, pos_x: int, pos_y: int, 
                         quantidade: int, local: str) -> bool:
        conexao = self.__banco_de_dados.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")
            
        try:
            cursor = conexao.cursor()
            
            # Converter local para numérico
            local_num = 0 if local == 'armazem' else 1
            
            # Verificar se posição está disponível
            cursor.execute("""
                SELECT id FROM t_estoque_armazem 
                WHERE id_mercado = ? AND local = ? AND pos_x = ? AND pos_y = ?
            """, (id_mercado, local_num, pos_x, pos_y))
            
            if cursor.fetchone():
                raise CustomException("Posição já ocupada")
            
            cursor.execute("""
                INSERT INTO t_estoque_armazem (id_produto, id_mercado, pos_x, pos_y, quantidade, local)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (id_produto, id_mercado, pos_x, pos_y, quantidade, local_num))
            
            conexao.commit()
            return True
            
        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Erro ao adicionar produto: {e}")
            raise CustomException("Erro ao adicionar produto")
        finally:
            if conexao:
                conexao.close()
    
    def remover_produto(self, id_item: int) -> bool:
        conexao = self.__banco_de_dados.get_connection()
        if not conexao:
            raise CustomException("Erro ao conectar com o banco de dados")
            
        try:
            cursor = conexao.cursor()
            
            cursor.execute("DELETE FROM t_estoque_armazem WHERE id = ?", (id_item,))
            
            conexao.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            print(f"Erro ao remover produto: {e}")
            raise CustomException("Erro ao remover produto")
        finally:
            if conexao:
                conexao.close()