import sqlite3
import os

class DatabaseConnection:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(current_dir, '../../resources/bancodedados.db')
        conn = self.get_connection()
        self._configurar_tabelas(conn)

        
    def get_connection(self):
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            print(f"Erro ao conectar com o banco: {e}")
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
            "motivo_demissao" VARCHAR,
            PRIMARY KEY("cpf")
            );""")
        
        # Verificar se a tabela está vazia antes de inserir
        cursor.execute("SELECT COUNT(*) as count FROM t_funcionario")
        resultado = cursor.fetchone()
        
        if resultado['count'] == 0:
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
                    "ativo"
                ) VALUES 
                (
                    '12345678901', 
                    'Gerente da Silva', 
                    '$2a$12$wQ8pOp2FnBS71EUj2loNq.vHNLOfUZFg7DuI05.97yBbnT.tWZEWu',
                    'gerente.silva@empresa.com', 
                    '1985-03-15',
                    '2020-01-10',
                    3500.00, 
                    0, 
                    1
                ),
                (
                    '12345678902', 
                    'Repositor Pedrosa', 
                    '$2a$12$wQ8pOp2FnBS71EUj2loNq.vHNLOfUZFg7DuI05.97yBbnT.tWZEWu',
                    'caixa.santos@empresa.com', 
                    '1990-07-22',
                    '2021-03-20',
                    4200.00, 
                    1, 
                    1
                ),
                (
                    '12345678903', 
                    'Caixa de Oliveira', 
                    '$2a$12$wQ8pOp2FnBS71EUj2loNq.vHNLOfUZFg7DuI05.97yBbnT.tWZEWu',
                    'repositor.oliveira@empresa.com', 
                    '1988-11-30',
                    '2019-08-05',
                    2800.00, 
                    2, 
                    1
                );
            """)
            conexao.commit()
        
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
        
        # t_produto - salva os dados de um produto
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_produto" (
                "id" INTEGER NOT NULL UNIQUE,
                "nome" VARCHAR NOT NULL,
                "marca" VARCHAR NOT NULL,
                "preco" FLOAT NOT NULL,
                PRIMARY KEY("id")
                );""")
        
        cursor.execute("SELECT COUNT(*) as count FROM t_produto")
        resultado = cursor.fetchone()
        
        if resultado['count'] == 0:
            cursor.executescript("""
                INSERT INTO "t_produto" ("id", "marca", "nome", "preco") VALUES
                    (1, 'Sadia', 'Peito de Frango', 18.90),
                    (2, 'Seara', 'Linguiça Calabresa', 12.50),
                    (3, 'Perdigão', 'Coxa e Sobrecoxa', 15.75),
                    (4, 'Sadia', 'Carne Moída', 24.90),
                    (5, 'Friboi', 'Picanha', 89.90),
                    (6, 'Seara', 'Filé de Frango', 22.40),
                    (7, 'Perdigão', 'Nuggets', 16.80),
                    (8, 'Sadia', 'Salsicha', 8.90),
                    (9, 'Friboi', 'Alcatra', 45.50),
                    (10, 'Seara', 'Hambúrguer Bovino', 19.90),
                    (11, 'Perdigão', 'Linguiça de Frango', 11.25),
                    (12, 'Sadia', 'Bacon', 14.30);
                """)
            
        # t_estoque - salvaos dados do estoque
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_estoque" (
                "id" INTEGER NOT NULL UNIQUE,
                "id_produto" INTEGER NOT NULL,
                "local" INTEGER NOT NULL,
                "pos_x" INTEGER NOT NULL,
                "pos_y" INTEGER NOT NULL,
                "quantidade" INTEGER NOT NULL,
                PRIMARY KEY("id"),
                FOREIGN KEY ("id_produto") REFERENCES "t_produto"("id")
                ON UPDATE NO ACTION ON DELETE NO ACTION
                );""")
        
        cursor.execute("SELECT COUNT(*) as count FROM t_estoque")
        resultado = cursor.fetchone()
        
        if resultado['count'] == 0:
            cursor.executescript("""
                INSERT INTO "t_estoque" ("id", "id_produto", "pos_x", "pos_y", "quantidade", "local") VALUES
                    (1, 1, 1, 1, 50, 0),
                    (2, 2, 1, 2, 30, 1),
                    (3, 3, 1, 3, 25, 0),
                    (4, 4, 1, 4, 40, 0),
                    (5, 5, 2, 1, 20, 0),
                    (6, 6, 2, 2, 35, 0),
                    (7, 7, 2, 3, 15, 0),
                    (8, 8, 2, 4, 60, 0),
                    (9, 9, 3, 1, 45, 0),
                    (10, 10, 3, 2, 28, 0),
                    (11, 11, 3, 3, 32, 0),
                    (12, 12, 3, 4, 18, 0);
                """)
                
        # t_pedido - salva os dados de um pedido
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_pedido" (
                "id" INTEGER NOT NULL UNIQUE,
                "id_responsavel" VARCHAR NOT NULL,
                "estado" INTEGER NOT NULL,
                PRIMARY KEY("id"),
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
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS t_vendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produto INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
                total REAL NOT NULL,
                codigo_pix VARCHAR(50) UNIQUE,
                FOREIGN KEY (id_produto) REFERENCES t_produto(id)
                );""")
        
        #t_vendas_produtos - salva os produtos do mercado que foram vendidos 
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_vendas_produtos" (
                "id" INTEGER NOT NULL UNIQUE,
                "id_venda"   INTEGER NOT NULL,
                "id_produto" INTEGER NOT NULL,
                "quantidade" INTEGER NOT NULL,
                PRIMARY KEY("id")
                );""")
