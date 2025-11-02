import sqlite3
import os

class DatabaseConnection:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(current_dir, '../../resources/bancodedados.db')
        
    def get_connection(self):
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            self._configurar_tabelas(conn)
            return conn
        except sqlite3.Error as e:
            print(f"❌ Erro ao conectar com o banco: {e}")
            return None
            
    def _configurar_tabelas(self, conexao: sqlite3.Connection):
        cursor = conexao.cursor()
        
        # t_funcionario - salva os dados dos usuarios
        cursor.execute("""CREATE TABLE IF NOT EXISTS "t_funcionario" (
            "cpf" VARCHAR NOT NULL UNIQUE,
            "nome" VARCHAR NOT NULL,
            "senha" VARCHAR NOT NULL,
            "email" VARCHAR NOT NULL,
            "data_nascimento" DATE NOT NULL,
            "data_admissao" DATE NOT NULL DEFAULT CURRENT_DATE,
            "salario" REAL NOT NULL DEFAULT 0,
            "tipo" INTEGER NOT NULL,
            "ativo" BOOLEAN NOT NULL DEFAULT 1,
            "id_supervisor" INTEGER NOT NULL,
            "motivo_demissao" VARCHAR,
            PRIMARY KEY("cpf")
            );""")
        
        # Verificar se a tabela está vazia antes de inserir
        cursor.execute("SELECT COUNT(*) as count FROM t_funcionario")
        resultado = cursor.fetchone()
        
        if resultado['count'] == 0:
            print("📝 Inserindo dados iniciais na tabela funcionarios...")
            # Inserir dados iniciais apenas se a tabela estiver vazia
            cursor.executescript("""
                INSERT INTO "t_funcionario" (
                    "cpf", 
                    "nome", 
                    "senha", 
                    "email", 
                    "data_nascimento", 
                    "data_admissao",
                    "salario", 
                    "tipo", 
                    "ativo", 
                    "id_supervisor"
                ) VALUES 
                (
                    '123.456.789-01', 
                    'João Silva', 
                    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lewd5g5Z5c1E5n5Ne',
                    'joao.silva@empresa.com', 
                    '1985-03-15',
                    '2020-01-10',
                    3500.00, 
                    1, 
                    1, 
                    0
                ),
                (
                    '234.567.890-12', 
                    'Maria Santos', 
                    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lewd5g5Z5c1E5n5Ne',
                    'maria.santos@empresa.com', 
                    '1990-07-22',
                    '2021-03-20',
                    4200.00, 
                    1, 
                    1, 
                    1
                ),
                (
                    '345.678.901-23', 
                    'Pedro Oliveira', 
                    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lewd5g5Z5c1E5n5Ne',
                    'pedro.oliveira@empresa.com', 
                    '1988-11-30',
                    '2019-08-05',
                    2800.00, 
                    2, 
                    1, 
                    1
                ),
                (
                    '456.789.012-34', 
                    'Ana Costa', 
                    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lewd5g5Z5c1E5n5Ne',
                    'ana.costa@empresa.com', 
                    '1992-05-18',
                    '2022-02-14',
                    3800.00, 
                    1, 
                    1, 
                    1
                ),
                (
                    '567.890.123-45', 
                    'Carlos Lima', 
                    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lewd5g5Z5c1E5n5Ne',
                    'carlos.lima@empresa.com', 
                    '1987-12-03',
                    '2020-11-08',
                    3200.00, 
                    2, 
                    1, 
                    1
                ),
                (
                    '678.901.234-56', 
                    'Juliana Pereira', 
                    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/Lewd5g5Z5c1E5n5Ne',
                    'juliana.pereira@empresa.com', 
                    '1991-09-25',
                    '2023-01-30',
                    2900.00, 
                    2, 
                    1, 
                    1
                );
            """)
            conexao.commit()
            print("✅ Dados iniciais inseridos com sucesso!")
        
        # t_ponto - salva os dados de ponto dos usuarios
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_ponto" (
                "id" INTEGER NOT NULL UNIQUE,
                "id_usuario" VARCHAR NOT NULL,
                "horario" DATETIME NOT NULL,
                "tipo" INTEGER NOT NULL,
                PRIMARY KEY("id"),
                FOREIGN KEY ("id_usuario") REFERENCES "t_funcionario"("cpf")
                ON UPDATE NO ACTION ON DELETE NO ACTION
                );""")
        
        # t_mercado - salva os dados de um mercado
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_mercado" (
                "id" INTEGER NOT NULL UNIQUE,
                "nome" INTEGER,
                "capacidade" INTEGER,
                "tam_armazem_x" INTEGER NOT NULL,
                "tam_armazem_y" INTEGER NOT NULL,
                "endereço" VARCHAR NOT NULL,
                PRIMARY KEY("id")
                );""")
        
        # t_estoque_mercado - salva os dados do estoque de um mercado
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_estoque_mercado" (
                "id" INTEGER NOT NULL UNIQUE,
                "id_mercado" INTEGER NOT NULL,
                "id_produto" INTEGER NOT NULL,
                "quantidade" INTEGER NOT NULL,
                PRIMARY KEY("id"),
                FOREIGN KEY ("id_produto") REFERENCES "t_produto"("id")
                ON UPDATE NO ACTION ON DELETE NO ACTION,
                FOREIGN KEY ("id_mercado") REFERENCES "t_mercado"("id")
                ON UPDATE NO ACTION ON DELETE NO ACTION
                );""")
        
        # t_estoque_armazem - salvaos dados do estoque de um armazem
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_estoque_armazem" (
                "id" INTEGER NOT NULL UNIQUE,
                "id_mercado" INTEGER NOT NULL,
                "id_produto" INTEGER NOT NULL,
                "pos_x" INTEGER NOT NULL,
                "pos_y" INTEGER NOT NULL,
                "quantidade" INTEGER NOT NULL,
                PRIMARY KEY("id"),
                FOREIGN KEY ("id_produto") REFERENCES "t_produto"("id")
                ON UPDATE NO ACTION ON DELETE NO ACTION,
                FOREIGN KEY ("id_mercado") REFERENCES "t_mercado"("id")
                ON UPDATE NO ACTION ON DELETE NO ACTION
                );""")
        
        # t_produto - salva os dados de um produto
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_produto" (
                "id" INTEGER NOT NULL UNIQUE,
                "nome" VARCHAR NOT NULL,
                "marca" VARCHAR NOT NULL,
                PRIMARY KEY("id")
                );""")
                
        # t_pedido - salva os dados de um pedido
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_pedido" (
                "id" INTEGER NOT NULL UNIQUE,
                "id_responsavel" VARCHAR NOT NULL,
                "id_mercado" INTEGER NOT NULL,
                "estado" INTEGER NOT NULL,
                PRIMARY KEY("id"),
                FOREIGN KEY ("id_mercado") REFERENCES "t_mercado"("id")
                ON UPDATE NO ACTION ON DELETE NO ACTION,
                FOREIGN KEY ("id_responsavel") REFERENCES "t_funcionario"("cpf")
                ON UPDATE NO ACTION ON DELETE NO ACTION
                );""")
        
        # t_pedido_produto - salva os dados dos produtos de um pedido
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_pedido_produto" (
                "id" INTEGER NOT NULL UNIQUE,
                "id_pedido" INTEGER,
                "id_produto" INTEGER NOT NULL,
                "quantidade" INTEGER NOT NULL,
                PRIMARY KEY("id"),
                FOREIGN KEY ("id_pedido") REFERENCES "t_pedido"("id")
                ON UPDATE NO ACTION ON DELETE NO ACTION,
                FOREIGN KEY ("id_produto") REFERENCES "t_produto"("id")
                ON UPDATE NO ACTION ON DELETE NO ACTION
                );""")
        
        #t_auth - salva dados de login
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_auth" (
                "id" INTEGER NOT NULL UNIQUE,
                "user" TEXT NOT NULL,
                "password" TEXT NOT NULL,
                PRIMARY KEY("id")
                );""")
        
        #t_vendas - salva dados de vendas
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_vendas" (
                "id" INTEGER NOT NULL UNIQUE,
                "id_responsavel" INTEGER NOT NULL,
                "time" INTEGER NOT NULL,
                PRIMARY KEY("id")
                );""")
        
        #t_vendas_produtos - salva os produtos do mercado que foram vendidos 
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_vendas_produtos" (
        "id_venda"   INTEGER NOT NULL,
        "id_produto" INTEGER NOT NULL,
        "quantidade" INTEGER NOT NULL,
        PRIMARY KEY("id_venda", "id_produto")
        );""")