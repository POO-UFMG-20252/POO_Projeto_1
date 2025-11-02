class CustomException(Exception):
    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem
            
    def to_dict(self):
        return vars(self)