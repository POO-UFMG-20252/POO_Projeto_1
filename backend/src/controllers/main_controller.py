from http.server import HTTPServer, BaseHTTPRequestHandler
from controllers.produto_controller import ProdutoController

class MainController():
    def __init__(self):
        self.port = 8000
        self.server_address = ('', self.port)
        self.httpd = HTTPServer(self.server_address, MainBaseHTTPRequestHandler)
    
    def serve(self):
        print(f"Iniciando servidor na porta {self.port}")
        self.httpd.serve_forever()
    
class MainBaseHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.controller_produtos = ProdutoController()
        super().__init__(request, client_address, server)
        
    def do_GET(self):
        try:
            subsistema = self.path.split("/")[3]
            if subsistema == self.controller_produtos.responsabilidade:
                return self.controller_produtos.do_GET(self)
            else:
                return self.send_response(404, "Not Found")
        except Exception as e:
            print(f"Houve um erro ao processar a requisicao GET: {self} | Exception: {e}")
            return self.send_response(500)
            
    def do_POST(self):
        try:
            subsistema = self.path.split("/")[2]
            if subsistema == self.controller_produtos.responsabilidade:
                return self.controller_produtos.do_GET(self)
            else:
                return self.send_response(404, "Not Found")
        except Exception as e:
            print(f"Houve um erro ao processar a requisicao GET: {self} | Exception: {e}")
            return self.send_response(500, "Internal Server Error")
    
    def carregar_controllers(self):
        self.controller_produtos = ProdutoController()
