from abc import ABC, abstractmethod

class AbstractController(ABC):
    def __init__(self, responsabilidade: str):
        self.responsabilidade = responsabilidade
    
    @abstractmethod
    def do_GET(self, mainController):
        pass
    
    @abstractmethod
    def do_POST(self, mainController):
        pass