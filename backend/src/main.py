from database.connection import DatabaseConnection

from services.impl.autenticacao_service_impl import AutenticacaoServiceImpl
from services.impl.funcionario_service_impl import FuncionarioServiceImpl

from controllers.main_app import MainApp
from controllers.autenticacao_controller import AutenticacaoController
from controllers.funcionario_controller import FuncionarioController

def main():
    conexaoBancoDeDados = DatabaseConnection()

    funcionarioService = FuncionarioServiceImpl(conexaoBancoDeDados)
    autenticacaoService = AutenticacaoServiceImpl(funcionarioService)
    
    autenticacaoController = AutenticacaoController(autenticacaoService)
    funcionarioController = FuncionarioController(funcionarioService)
    
    controllers = [
        autenticacaoController,
        funcionarioController
    ]
    
    app = MainApp(controllers)
    app.run()
    
main()