class ControllerError:
    def __init__(self, mensagem):
        self.mensagem = mensagem
        
    def to_dict(self):
        return vars(self)