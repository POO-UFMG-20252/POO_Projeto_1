from database.connection import DatabaseConnection

from services.autenticacao_service import AutenticacaoService

from controllers.main_app import MainApp
from controllers.autenticacao_controller import AutenticacaoController

def main():
    conexaoBancoDeDados = DatabaseConnection()

    autenticacaoService = AutenticacaoService(conexaoBancoDeDados)
    
    autenticacaoController = AutenticacaoController(autenticacaoService)
    
    controllers = [
        autenticacaoController
    ]
    
    app = MainApp(controllers)
    app.run()