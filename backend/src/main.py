from database.connection import DatabaseConnection

from services.impl.autenticacao_service_impl import AutenticacaoServiceImpl
from services.impl.funcionario_service_impl import FuncionarioServiceImpl
from services.impl.estoque_service_impl import EstoqueServiceImpl
from services.impl.caixa_service_impl import CaixaServiceImpl  

from controllers.main_app import MainApp
from controllers.autenticacao_controller import AutenticacaoController
from controllers.funcionario_controller import FuncionarioController
from controllers.estoque_controller import EstoqueController
from controllers.caixa_controller import CaixaController  

def main():
    conexaoBancoDeDados = DatabaseConnection()

    funcionarioService = FuncionarioServiceImpl(conexaoBancoDeDados)
    estoqueService = EstoqueServiceImpl(conexaoBancoDeDados)
    caixaService = CaixaServiceImpl(conexaoBancoDeDados)
    autenticacaoService = AutenticacaoServiceImpl(funcionarioService)
    
    autenticacaoController = AutenticacaoController(autenticacaoService)
    funcionarioController = FuncionarioController(funcionarioService)
    estoqueController = EstoqueController(estoqueService)
    caixaController = CaixaController(caixaService)  
    
    controllers = [
        autenticacaoController,
        funcionarioController,
        estoqueController,
        caixaController  
    ]
    
    app = MainApp(controllers)
    app.run()
    
main()