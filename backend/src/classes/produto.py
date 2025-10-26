import sqlite3
DB_NAME = "database.db"
class Produto():
	def __init__(self, id, nome, marca):
		self.id = id
		self.nome = nome
		self.marca = marca
	#getters e setters nome
	@property
	def nome(self):
		return self._nome
	@nome.setter
	def nome(self, nome_novo):
		self._nome = nome_novo

	#getters e setters marca
	@property
	def marca(self):
		return self._marca
	@marca.setter
	def marca(self, marca_nova):
		self._marca = marca_nova
	
	#getter id
	@property
	def id(self):
		return self._id
	
	#setter id(opcional)
	@id.setter
	def id(self,id_novo):
		self_id = id_novo
	
	
	@staticmethod
	def salvar_produto(produto):
		with sqlite3.connect(DB_NAME) as con:
			cur = con.cursor()
			cur.execute("INSERT INTO t_produto (id,nome,marca) VALUES (?, ?,?)", (produto.id,produto.nome,produto.marca))
			con.commit()

	@staticmethod
	def remover_produto(produto):
		with sqlite3.connect(DB_NAME) as con:
			cur = con.cursor()
			cur.execute("DELETE FROM t_produto WHERE id =?",(produto.id))
	
	@staticmethod
	def busca_produto(produto_id):
		try:
			with sqlite3.connect(DB_NAME) as con:
				cur = con.cursor()
				cur.execute("SELECT id,nome,marca FROM t_produto WHERE id =?",(produto_id))
				result = cur.fetchone()
				return result
		except:
			return None
	
	@staticmethod
	def busca_geral():
		produtos = [] #array final/geral
		try:
			with sqlite3.connect(DB_NAME) as con:
				cur = con.cursor()
				cur.execute("SELECT id,nome,marca FROM t_produto ")
				results = cur.fetchall()#pega todos os produtos
				for result in results:
					produto = Produto(*result)
					produtos.append(produto)#pega cada item do fetchall e salva como um objeto na lista produtos
			return produtos
		except:
			return []#retorna lista vazia caso de erro
