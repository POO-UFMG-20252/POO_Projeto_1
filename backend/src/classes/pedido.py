class Pedido():
    def __init__(self, id,id_responsavel,id_mercado,estado):
        self.id = id
        self.id_responsavel = id_responsavel
        self.id_mercado = id_mercado
        self.estado = estado

    #getters e setters id
    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, id_novo):
        self._id = id_novo

    #getters e setters id_responsavel
    @property
    def id_responsavel(self):
        return self._id_responsavel
    @id_responsavel.setter
    def id_responsavel(self,id_responsavel_novo):
        self._id_responsavel = id_responsavel_novo

    #getters e setters id_mercado
    @property
    def id_mercado(self):
        return self.id_mercado
    @id_mercado.setter
    def id_mercado(self,id_mercado_novo):
        self._id_mercado = id_mercado_novo

    #getters e setters estado
    @property
    def estado(self):
        return self.estado
    @estado.setter
    def estado(self,estado_novo):
        self._estado = estado_novo