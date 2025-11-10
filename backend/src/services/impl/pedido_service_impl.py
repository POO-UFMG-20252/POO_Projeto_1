from sqlite3 import Connection
from typing import List 
from database.connection import DatabaseConnection
from classes.custom_exception import CustomException
from classes.pedido import Pedido
from services.pedido_service import PedidoService

class PedidoServiceImpl(PedidoService):
    def __init__(self, banco_de_dados: DatabaseConnection):
        self.__banco_de_dados = banco_de_dados

    def adicionar_pedido(self, id_responsavel: str, estado: int, lista_produtos: list[list]) -> Pedido:
        conexao = None
        try:
            conexao = self.__banco_de_dados.get_connection()
            if not conexao:
                raise CustomException("Erro ao conectar com o banco de dados")
            
            cursor = conexao.cursor()
            
            # Iniciar transação
            cursor.execute("BEGIN TRANSACTION")
            
            try:
                # 1. Criar o pedido
                cursor.execute("""
                    INSERT INTO t_pedido (id_responsavel, estado)
                    VALUES (?, ?)
                """, (id_responsavel, estado))
                
                pedido_id = cursor.lastrowid
                
                # 2. Processar cada produto da lista
                for produto_info in lista_produtos:
                    if len(produto_info) != 4:
                        raise CustomException("Formato inválido para produto")
                    
                    nome, marca, preco, quantidade = produto_info
                    
                    # Verificar se o produto já existe
                    cursor.execute("""
                        SELECT id FROM t_produto 
                        WHERE nome = ? AND marca = ?
                    """, (nome, marca))
                    
                    produto_existente = cursor.fetchone()
                    
                    if produto_existente:
                        produto_id = produto_existente['id']
                    else:
                        # Criar novo produto
                        cursor.execute("""
                            INSERT INTO t_produto (nome, marca, preco)
                            VALUES (?, ?, ?)
                        """, (nome, marca, float(preco)))
                        produto_id = cursor.lastrowid
                    
                    # 3. Adicionar ao t_pedido_produto
                    cursor.execute("""
                        INSERT INTO t_pedido_produto (id_pedido, id_produto, quantidade)
                        VALUES (?, ?, ?)
                    """, (pedido_id, produto_id, int(quantidade)))
                
                # Commit da transação
                cursor.execute("COMMIT")
                
                # Buscar pedido criado
                return self.buscar_pedido(pedido_id)
                
            except Exception as e:
                cursor.execute("ROLLBACK")
                raise e
                
        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Erro ao adicionar pedido: {e}")
            raise CustomException("Erro ao criar pedido")
        finally:
            if conexao:
                conexao.close()
    
    def editar_pedido(self, id: int, estado: int) -> Pedido:
        conexao = None
        try:
            conexao = self.__banco_de_dados.get_connection()
            if not conexao:
                raise CustomException("Erro ao conectar com o banco de dados")
            
            cursor = conexao.cursor()
            
            # Verificar se pedido existe
            cursor.execute("SELECT * FROM t_pedido WHERE id = ?", (id,))
            if not cursor.fetchone():
                raise CustomException("Pedido não encontrado")
            
            # Atualizar estado
            cursor.execute("""
                UPDATE t_pedido 
                SET estado = ? 
                WHERE id = ?
            """, (estado, id))
            
            conexao.commit()
            
            return self.buscar_pedido(id)
            
        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Erro ao editar pedido: {e}")
            raise CustomException("Erro ao editar pedido")
        finally:
            if conexao:
                conexao.close()
    
    def remover_pedido(self, id: int) -> Pedido:
        conexao = None
        try:
            conexao = self.__banco_de_dados.get_connection()
            if not conexao:
                raise CustomException("Erro ao conectar com o banco de dados")
            
            cursor = conexao.cursor()
            
            # Buscar pedido antes de remover
            pedido = self.buscar_pedido(id)
            if not pedido:
                raise CustomException("Pedido não encontrado")
            
            # Iniciar transação
            cursor.execute("BEGIN TRANSACTION")
            
            try:
                # Remover da t_pedido_produto
                cursor.execute("DELETE FROM t_pedido_produto WHERE id_pedido = ?", (id,))
                
                # Remover da t_pedido
                cursor.execute("DELETE FROM t_pedido WHERE id = ?", (id,))
                
                cursor.execute("COMMIT")
                
                return pedido
                
            except Exception as e:
                cursor.execute("ROLLBACK")
                raise e
                
        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Erro ao remover pedido: {e}")
            raise CustomException("Erro ao remover pedido")
        finally:
            if conexao:
                conexao.close()
    
    def buscar_pedido(self, id: int) -> Pedido:
        conexao = None
        try:
            conexao = self.__banco_de_dados.get_connection()
            if not conexao:
                raise CustomException("Erro ao conectar com o banco de dados")
            
            cursor = conexao.cursor()
            
            # Buscar dados do pedido
            cursor.execute("""
                SELECT p.id, p.id_responsavel, p.estado, f.nome as responsavel_nome
                FROM t_pedido p
                LEFT JOIN t_funcionario f ON p.id_responsavel = f.cpf
                WHERE p.id = ?
            """, (id,))
            
            pedido_data = cursor.fetchone()
            
            if not pedido_data:
                return None
            
            # Buscar produtos do pedido
            cursor.execute("""
                SELECT pp.id_produto, pp.quantidade, pr.nome, pr.marca, pr.preco
                FROM t_pedido_produto pp
                JOIN t_produto pr ON pp.id_produto = pr.id
                WHERE pp.id_pedido = ?
            """, (id,))
            
            produtos_data = cursor.fetchall()
            
            # Criar lista de produtos
            produtos = []
            for produto in produtos_data:
                produtos.append({
                    'id_produto': produto['id_produto'],
                    'nome': produto['nome'],
                    'marca': produto['marca'],
                    'preco': produto['preco'],
                    'quantidade': produto['quantidade']
                })
            
            # CORREÇÃO: Usar estado correto (não [0])
            return Pedido(
                id=pedido_data['id'],
                id_responsavel=pedido_data['id_responsavel'],
                estado=pedido_data['estado'],  # CORREÇÃO AQUI
                produtos=produtos
            )
            
        except Exception as e:
            print(f"Erro ao buscar pedido: {e}")
            raise CustomException("Erro ao buscar pedido")
        finally:
            if conexao:
                conexao.close()
                
    def listar_pedidos(self) -> List[Pedido]:
        conexao = None
        try:
            conexao = self.__banco_de_dados.get_connection()
            if not conexao:
                raise CustomException("Erro ao conectar com o banco de dados")

            cursor = conexao.cursor()

            # Buscar todos os pedidos
            cursor.execute("""
                SELECT 
                    p.id,
                    p.id_responsavel,
                    p.estado,
                    f.nome as responsavel_nome
                FROM t_pedido p
                LEFT JOIN t_funcionario f ON p.id_responsavel = f.cpf
                ORDER BY p.id DESC
            """)

            pedidos_data = cursor.fetchall()
            pedidos = []

            for pedido_row in pedidos_data:
                # Para listar pedidos, não precisamos dos produtos, apenas dados básicos
                # Criar lista vazia de produtos para manter a compatibilidade
                produtos = []

                # CORREÇÃO: Usar estado correto (não [0])
                pedido = Pedido(
                    id=pedido_row['id'],
                    id_responsavel=pedido_row['id_responsavel'],
                    estado=pedido_row['estado'],  # CORREÇÃO AQUI
                    produtos=produtos
                )

                pedidos.append(pedido)

            return pedidos

        except Exception as e:
            print(f"Erro ao listar pedidos: {e}")
            raise CustomException("Erro ao buscar lista de pedidos")
        finally:
            if conexao:
                conexao.close()
                
    def alterar_estado_pedido(self, id: int, novo_estado: int) -> Pedido:
        conexao = None
        try:
            conexao = self.__banco_de_dados.get_connection()
            if not conexao:
                raise CustomException("Erro ao conectar com o banco de dados")

            cursor = conexao.cursor()

            # Verificar se o pedido existe e buscar estado atual
            cursor.execute("SELECT * FROM t_pedido WHERE id = ?", (id,))
            pedido_existente = cursor.fetchone()

            if not pedido_existente:
                raise CustomException("Pedido não encontrado")

            estado_atual = pedido_existente['estado']

            # Validar o novo estado
            if novo_estado not in [0, 1, 2, 3]:
                raise CustomException("Estado inválido. Use: 0=Aguardando, 1=A caminho, 2=Entregue, 3=Finalizado")

            # Iniciar transação
            cursor.execute("BEGIN TRANSACTION")

            try:
                # Se está mudando de Entregue (2) para Finalizado (3), armazenar no estoque
                if estado_atual == 2 and novo_estado == 3:
                    self._armazenar_produtos_no_estoque(cursor, id)

                # Atualizar o estado do pedido
                cursor.execute("""
                    UPDATE t_pedido 
                    SET estado = ? 
                    WHERE id = ?
                """, (novo_estado, id))

                cursor.execute("COMMIT")

            except Exception as e:
                cursor.execute("ROLLBACK")
                raise e

            # Retornar o pedido atualizado
            return self.buscar_pedido(id)

        except CustomException as e:
            raise e
        except Exception as e:
            print(f"Erro ao alterar estado do pedido: {e}")
            raise CustomException("Erro ao alterar estado do pedido")
        finally:
            if conexao:
                conexao.close()

    def _armazenar_produtos_no_estoque(self, cursor, pedido_id: int):   
        # Buscar todos os produtos do pedido
        cursor.execute("""
            SELECT pp.id_produto, pp.quantidade, pr.nome
            FROM t_pedido_produto pp
            JOIN t_produto pr ON pp.id_produto = pr.id
            WHERE pp.id_pedido = ?
        """, (pedido_id,))
        
        produtos_pedido = cursor.fetchall()
        
        if not produtos_pedido:
            raise CustomException("Nenhum produto encontrado no pedido")
        
        # Buscar posições ocupadas no estoque para a matriz 5x5
        cursor.execute("""
            SELECT pos_x, pos_y 
            FROM t_estoque 
            WHERE local = 0
        """)
        
        posicoes_ocupadas = cursor.fetchall()
        posicoes_set = set((pos['pos_x'], pos['pos_y']) for pos in posicoes_ocupadas)
        
        # Gerar todas as posições possíveis da matriz 5x5
        todas_posicoes = []
        for x in range(1, 6):  # 1 a 5
            for y in range(1, 6):  # 1 a 5
                todas_posicoes.append((x, y))
        
        # Encontrar posições livres
        posicoes_livres = [pos for pos in todas_posicoes if pos not in posicoes_set]
        
        if len(posicoes_livres) < len(produtos_pedido):
            raise CustomException("Espaço insuficiente no estoque para armazenar todos os produtos")
        
        # Buscar o próximo ID disponível para t_estoque
        cursor.execute("SELECT MAX(id) as max_id FROM t_estoque")
        resultado = cursor.fetchone()
        proximo_id = resultado['max_id'] + 1 if resultado['max_id'] else 1
        
        # Armazenar cada produto no estoque
        for i, produto in enumerate(produtos_pedido):
            pos_x, pos_y = posicoes_livres[i]
            
            # Verificar se o produto já existe nessa posição
            cursor.execute("""
                SELECT id, quantidade 
                FROM t_estoque 
                WHERE id_produto = ? AND pos_x = ? AND pos_y = ? AND local = 0
            """, (produto['id_produto'], pos_x, pos_y))
            
            produto_existente = cursor.fetchone()
            
            if produto_existente:
                # Se já existe, atualizar a quantidade
                cursor.execute("""
                    UPDATE t_estoque 
                    SET quantidade = quantidade + ? 
                    WHERE id = ?
                """, (produto['quantidade'], produto_existente['id']))
            else:
                # Se não existe, inserir novo registro
                cursor.execute("""
                    INSERT INTO t_estoque (id, id_produto, local, pos_x, pos_y, quantidade)
                    VALUES (?, ?, 0, ?, ?, ?)
                """, (proximo_id, produto['id_produto'], pos_x, pos_y, produto['quantidade']))
                proximo_id += 1
    