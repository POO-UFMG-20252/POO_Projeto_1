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