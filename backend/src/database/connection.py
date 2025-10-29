import sqlite3
import os

class DatabaseConnection:
    def __init__(self):
        # Caminho absoluto para o banco de dados
        current_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(current_dir, 'estoque.db')
        
    def get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        try:
            # Garantir que o diretório existe
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            
            # Verificar e criar tabela se não existir
            self._verificar_tabela(conn)
            
            return conn
        except sqlite3.Error as e:
            print(f"❌ Erro ao conectar com o banco: {e}")
            return None
    
    def _verificar_tabela(self, conn):
        """Verifica se a tabela existe e cria se necessário"""
        try:
            cursor = conn.cursor()
            
            # Verificar se a tabela existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='estoque'")
            if not cursor.fetchone():
                print("📋 Criando tabela 'estoque'...")
                cursor.execute('''
                CREATE TABLE estoque (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,
                    localizacao TEXT NOT NULL,
                    linha INTEGER NOT NULL,
                    coluna INTEGER NOT NULL
                )
                ''')
                
                # Inserir dados iniciais
                dados_iniciais = [
                    ('Refrigerante Lata', 300, 'armazem', 0, 0),
                    ('Água Mineral', 450, 'armazem', 0, 1),
                    ('Suco Natural', 200, 'armazem', 1, 2),
                    ('Energético', 480, 'armazem', 2, 1),
                    ('Chá Gelado', 150, 'armazem', 3, 3),
                    ('Refrigerante 2L', 350, 'loja', 0, 0),
                    ('Cerveja', 500, 'loja', 1, 1),
                    ('Água com Gás', 280, 'loja', 2, 2)
                ]
                
                cursor.executemany('''
                INSERT INTO estoque (nome, quantidade, localizacao, linha, coluna)
                VALUES (?, ?, ?, ?, ?)
                ''', dados_iniciais)
                
                conn.commit()
                print(f"✅ Tabela criada e {len(dados_iniciais)} registros inseridos!")
            else:
                print("✅ Tabela 'estoque' verificada!")
                
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
            if not cursor.fetchone():
                print("📋 Criando tabela 'usuarios'...")
                cursor.execute('''
                CREATE TABLE usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
	            nome TEXT UNIQUE NOT NULL,
                cpf TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL,
                cargo INTEGER NOT NULL, -- 0: Gerente, 1: Repositor, 2: Caixa
                ativo BOOLEAN DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                
                # Inserir usuário padrão
                cursor.execute('''
                INSERT INTO usuarios (cpf, nome, email, senha, cargo) VALUES 
                ('11111111111', 'Gabriela', 'gerente1@email.com', 'senha123', 0),
                ('22222222222', 'Jaime','gerente2@email.com', 'senha123', 0),
                ('33333333333', 'Lucas' ,'repositor1@email.com', 'senha123', 1),
                ('44444444444', 'Luigi' ,'repositor2@email.com', 'senha123', 1),
                ('55555555555', 'Artur' ,'caixa1@email.com', 'senha123', 2),
                ('66666666666', 'Gil' ,'caixa2@email.com', 'senha123', 2);
                ''')
                
                conn.commit()
                print("✅ Tabela 'usuarios' criada e usuário padrão inserido!")
            else:
                print("✅ Tabela 'usuarios' verificada!")
                
        except Exception as e:
            print(f"❌ Erro ao verificar tabela: {e}")
            conn.rollback()