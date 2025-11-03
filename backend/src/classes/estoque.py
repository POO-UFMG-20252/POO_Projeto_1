class ItemEstoque:
    def __init__(self, id: int, id_produto: int, pos_x: int, pos_y: int, 
                quantidade: int, produto_nome: str = "", local: str = "armazem"):
        self.__id = id
        self.__id_produto = id_produto
        self.__pos_x = pos_x
        self.__pos_y = pos_y
        self.__quantidade = quantidade
        self.__produto_nome = produto_nome
        self.__local = local
    
    # Getters e setters
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id_novo):
        self.__id = id_novo
    
    @property
    def id_produto(self):
        return self.__id_produto
    
    @id_produto.setter
    def id_produto(self, id_produto_novo):
        self.__id_produto = id_produto_novo
    
    @property
    def pos_x(self):
        return self.__pos_x
    
    @pos_x.setter
    def pos_x(self, pos_x_novo):
        self.__pos_x = pos_x_novo
    
    @property
    def pos_y(self):
        return self.__pos_y
    
    @pos_y.setter
    def pos_y(self, pos_y_novo):
        self.__pos_y = pos_y_novo
    
    @property
    def quantidade(self):
        return self.__quantidade
    
    @quantidade.setter
    def quantidade(self, quantidade_nova):
        if quantidade_nova < 0:
            raise ValueError("Quantidade não pode ser negativa")
        self.__quantidade = quantidade_nova
    
    @property
    def produto_nome(self):
        return self.__produto_nome
    
    @produto_nome.setter
    def produto_nome(self, produto_nome_novo):
        self.__produto_nome = produto_nome_novo
    
    @property
    def local(self):
        return self.__local
    
    @local.setter
    def local(self, local_novo):
        if local_novo not in ['armazem', 'loja']:
            raise ValueError("Local deve ser 'armazem' ou 'loja'")
        self.__local = local_novo
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_produto': self.id_produto,
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