from controllers.abstract_controller import AbstractController

class ProdutoController(AbstractController):
    def __init__(self):
        super().__init__(responsabilidade="produtos")

    def do_GET(self, mainController):
        if mainController.path == "/api/v1/produtos":
            print("Cheguei aqui A")
            mainController.send_response(200)
            mainController.send_header('Content-type', 'text/html')
            mainController.end_headers()
            mainController.wfile.write('<HTML><body>Hello World!</body></HTML>')
            return
        else:
            return mainController.send_response(404, "Not Found")
    
    def do_POST(self, mainController):
        if mainController.path == "/api/v1/produtos":
            print("Cheguei aqui B")
        else:
            return mainController.send_response(404, "Not Found")