from database.connection import DatabaseConnection

from services.impl.autenticacao_service_impl import AutenticacaoServiceImpl
from services.impl.funcionario_service_impl import FuncionarioServiceImpl

from controllers.main_app import MainApp
from controllers.autenticacao_controller import AutenticacaoController

def main():
    conexaoBancoDeDados = DatabaseConnection()

    funcionarioService = FuncionarioServiceImpl(conexaoBancoDeDados)
    autenticacaoService = AutenticacaoServiceImpl(funcionarioService)
    
    autenticacaoController = AutenticacaoController(autenticacaoService)
    
    controllers = [
        autenticacaoController
    ]
    
    app = MainApp(controllers)
    app.run()
    
main()