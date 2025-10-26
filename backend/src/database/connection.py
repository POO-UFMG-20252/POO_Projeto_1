import sqlite3
class DatabaseConnection:
    def __init__(self):
        self.connection = sqlite3.connect("./resources/database.db")
        self.cursor = self.connection.cursor()
        
    def configureDatabase(self):
        # t_usuario - salva os dados dos usuarios
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "t_usuario" (
                "id" VARCHAR NOT NULL UNIQUE,
                "nome" VARCHAR NOT NULL,
                "senha" VARCHAR NOT NULL,
                "email" VARCHAR NOT NULL,
                "data_nascimento" DATE NOT NULL,
                "salario" REAL NOT NULL DEFAULT 0,
                "tipo" INTEGER NOT NULL,
                "ativo" BOOLEAN NOT NULL,
                "id_supervisor" INTEGER NOT NULL,
                "motivo_demissao" VARCHAR,
                PRIMARY KEY("id")
                );""")
        
        # t_ponto - salva os dados de ponto dos usuarios
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "t_ponto" (
                "id" INTEGER NOT NULL UNIQUE,
                "id_usuario" VARCHAR NOT NULL,
                "horario" DATETIME NOT NULL,
                "tipo" INTEGER NOT NULL,
                PRIMARY KEY("id"),
                FOREIGN KEY ("id_usuario") REFERENCES "t_usuario"("id")
                ON UPDATE NO ACTION ON DELETE NO ACTION
                );""")
        
        # t_mercado - salva os dados de um mercado
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "t_mercado" (
                "id" INTEGER NOT NULL UNIQUE,
                "nome" INTEGER,
                "capacidade" INTEGER,
                "tam_armazem_x" INTEGER NOT NULL,
                "tam_armazem_y" INTEGER NOT NULL,
                "endereço" VARCHAR NOT NULL,
                PRIMARY KEY("id")
                );""")
        
        # t_estoque_mercado - salva os dados do estoque de um mercado
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "t_estoque_mercado" (
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
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "t_estoque_armazem" (
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
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "t_produto" (
                "id" INTEGER NOT NULL UNIQUE,
                "nome" VARCHAR NOT NULL,
                "marca" VARCHAR NOT NULL,
                PRIMARY KEY("id")
                );""")
        
        self.cursor.execute("""INSERT INTO t_produto (id, nome, marca) VALUES (1, leite, itambe)""")
        
        # t_pedido - salva os dados de um pedido
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "t_pedido" (
                "id" INTEGER NOT NULL UNIQUE,
                "id_responsavel" VARCHAR NOT NULL,
                "id_mercado" INTEGER NOT NULL,
                "estado" INTEGER NOT NULL,
                PRIMARY KEY("id"),
                FOREIGN KEY ("id_mercado") REFERENCES "t_mercado"("id")
                ON UPDATE NO ACTION ON DELETE NO ACTION,
                FOREIGN KEY ("id_responsavel") REFERENCES "t_usuario"("id")
                ON UPDATE NO ACTION ON DELETE NO ACTION
                );""")
        
        # t_pedido_produto - salva os dados dos produtos de um pedido
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "t_pedido_produto" (
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
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS "t_auth" (
                "id" INTEGER NOT NULL UNIQUE,
                "user" TEXT NOT NULL,
                "password" TEXT NOT NULL,
                PRIMARY KEY("id"),
                );""")
