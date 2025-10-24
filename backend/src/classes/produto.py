class Produto():
	def __init__(self, id, nome, marca):
		self.id = id
		self.nome = nome
		self.marca = marca
	
	@staticmethod
	def salvar_produto(produto):
     