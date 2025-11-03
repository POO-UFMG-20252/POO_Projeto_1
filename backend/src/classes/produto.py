class Produto:
    def __init__(self, id: int, nome: str, marca: str = "", preco: float = 0.0):
        self.__id = id
        self.__nome = nome
        self.__marca = marca
        self.__preco = preco
    
    # Getters e setters nome
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome_novo):
        self.__nome = nome_novo

    # Getters e setters marca
    @property
    def marca(self):
        return self.__marca
    
    @marca.setter
    def marca(self, marca_nova):
        self.__marca = marca_nova
    
    # Getter id
    @property
    def id(self):
        return self.__id
    
    # Setter id (opcional)
    @id.setter
    def id(self, id_novo):
        self.__id = id_novo
    
    # Getters e setters preco
    @property
    def preco(self):
        return self.__preco
    
    @preco.setter
    def preco(self, preco_novo):
        if preco_novo < 0:
            raise ValueError("Preço não pode ser negativo")
        self.__preco = preco_novo
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'marca': self.marca,
            'preco': self.preco
        }
    
    @staticmethod
    def from_dict(dict):
        return Produto(
            id=dict['id'],
            nome=dict['nome'],
            marca=dict['marca'],
            preco=dict['preco']
        )
    
    def __str__(self):
        return f"Produto(id={self.id}, nome='{self.nome}', marca='{self.marca}', preco={self.preco})"
    
    def __repr__(self):
        return self.__str__()