from flask import Flask
from controllers.produto_controller import ProdutoController

class MainApp:
    def __init__(self, controllers):
        self.app = Flask(__name__)
        self.controllers = controllers
        self._registrar_controllers()
        
    def _registrar_controllers(self):
        for controller in self.controllers:
            controller.registrar_rotas(self.app)
        print("Registro de rotas concluído.")
        
    def run(self, host='0.0.0.0', port=5000, debug=True):
        print(f"Iniciando servidor em http://{host}:{port}")
        self.app.run(host=host, port=port, debug=debug)