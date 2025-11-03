class CustomException(Exception):
    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.__mensagem = mensagem
    
    @property
    def mensagem(self):
        return self.__mensagem
    
    def to_dict(self):
        return vars(self)