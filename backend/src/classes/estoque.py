class ItemEstoque:
    def __init__(self, id: int, id_produto: int, id_mercado: int, pos_x: int, pos_y: int, 
                 quantidade: int, produto_nome: str = "", local: str = "armazem"):
        self._id = id
        self._id_produto = id_produto
        self._id_mercado = id_mercado
        self._pos_x = pos_x
        self._pos_y = pos_y
        self._quantidade = quantidade
        self._produto_nome = produto_nome
        self._local = local
    
    # Getters e setters
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id_novo):
        self._id = id_novo
    
    @property
    def id_produto(self):
        return self._id_produto
    
    @id_produto.setter
    def id_produto(self, id_produto_novo):
        self._id_produto = id_produto_novo
    
    @property
    def id_mercado(self):
        return self._id_mercado
    
    @id_mercado.setter
    def id_mercado(self, id_mercado_novo):
        self._id_mercado = id_mercado_novo
    
    @property
    def pos_x(self):
        return self._pos_x
    
    @pos_x.setter
    def pos_x(self, pos_x_novo):
        self._pos_x = pos_x_novo
    
    @property
    def pos_y(self):
        return self._pos_y
    
    @pos_y.setter
    def pos_y(self, pos_y_novo):
        self._pos_y = pos_y_novo
    
    @property
    def quantidade(self):
        return self._quantidade
    
    @quantidade.setter
    def quantidade(self, quantidade_nova):
        if quantidade_nova < 0:
            raise ValueError("Quantidade não pode ser negativa")
        self._quantidade = quantidade_nova
    
    @property
    def produto_nome(self):
        return self._produto_nome
    
    @produto_nome.setter
    def produto_nome(self, produto_nome_novo):
        self._produto_nome = produto_nome_novo
    
    @property
    def local(self):
        return self._local
    
    @local.setter
    def local(self, local_novo):
        if local_novo not in ['armazem', 'loja']:
            raise ValueError("Local deve ser 'armazem' ou 'loja'")
        self._local = local_novo
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_produto': self.id_produto,
            'id_mercado': self.id_mercado,
            'pos_x': self.pos_x,
            'pos_y': self.pos_y,
            'quantidade': self.quantidade,
            'produto_nome': self.produto_nome,
            'local': self.local
        }
    
    def __str__(self):
        return f"ItemEstoque(id={self.id}, produto='{self.produto_nome}', quantidade={self.quantidade}, local={self.local}, posição=({self.pos_x},{self.pos_y}))"
    
    def __repr__(self):
        return self.__str__()