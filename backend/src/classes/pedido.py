class Pedido():
    def __init__(self, id, id_responsavel, estado, produtos):
        self.__id = id
        self.__id_responsavel = id_responsavel
        self.__estado = estado
        self.__lista_produtos = produtos

    #getters e setters id
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, id_novo):
        self.__id = id_novo

    #getters e setters id_responsavel
    @property
    def id_responsavel(self):
        return self.__id_responsavel
    @id_responsavel.setter
    def id_responsavel(self,id_responsavel_novo):
        self.__id_responsavel = id_responsavel_novo

    #getters e setters estado
    @property
    def estado(self):
        return self.__estado
    @estado.setter
    def estado(self,estado_novo):
        self.__estado = estado_novo
        
    #getters e setters lista_produtos
    @property
    def lista_produtos(self):
        return self.lista_produtos
    @estado.setter
    def lista_produtos(self, lista_produtos):
        self.__lista_produtos = lista_produtos