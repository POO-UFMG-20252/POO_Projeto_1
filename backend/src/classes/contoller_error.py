from classes.custom_exception import CustomException

class ControllerError:
    def __init__(self, mensagem: str):
        self.__mensagem = mensagem

    @staticmethod
    def de_excecao(customException: CustomException):
        return ControllerError(customException.mensagem)

    def to_dict(self):
        return vars(self)