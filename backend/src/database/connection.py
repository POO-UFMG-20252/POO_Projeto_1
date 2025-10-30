import sqlite3
import os

class DatabaseConnection:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(current_dir, '../../resources/bancodedados.db')
        
    def get_connection(self):
        try:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            self._configurar_tabelas(conn)
        
            return conn
        except sqlite3.Error as e:
            print(f"❌ Erro ao conectar com o banco: {e}")
            return None
            
    def _configurar_tabelas(self, conexao: sqlite3.Connection):
        # t_funcionario - salva os dados dos usuarios
        conexao.cursor().execute("""CREATE TABLE IF NOT EXISTS "t_funcionario" (
                "cpf" VARCHAR NOT NULL UNIQUE,
                "nome" VARCHAR NOT NULL,
                "senha" VARCHAR NOT NULL,
                "email" VARCHAR NOT NULL,
                "data_nascimento" DATE NOT NULL,
                "salario" REAL NOT NULL DEFAULT 0,
                "tipo" INTEGER NOT NULL,
                "ativo" BOOLEAN NOT NULL,
                "id_supervisor" INTEGER NOT NULL,
                "motivo_demissao" VARCHAR,
                PRIMARY KEY("cpf")
                );""")
        
        conexao.cursor().execute("""INSERT INTO "t_funcionario" (
                "cpf", 
                "nome", 
                "senha", 
                "email", 
                "data_nascimento", 
                "salario", 
                "tipo", 
                "ativo", 
                "id_supervisor", 
                "motivo_demissao"
            ) VALUES (
                '12345678900',
                'Carlos Andrade',
                '$2a$12$k4Af3vdw7RiQuDU8K1Oi..Ex2kDpjoZndRMvKQGYpD5E/lBqkvtK2',
                'carlos.andrade@email.com',
                '1990-07-15',
                8200.00,
                1,
                1,
                101,
                NULL);""")
        
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