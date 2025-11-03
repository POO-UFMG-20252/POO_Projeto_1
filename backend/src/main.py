from database.connection import DatabaseConnection

from services.impl.autenticacao_service_impl import AutenticacaoServiceImpl
from services.impl.estoque_service_impl import EstoqueServiceImpl
from services.impl.funcionario_service_impl import FuncionarioServiceImpl
from services.impl.pedido_service_impl import PedidoServiceImpl
from services.impl.produto_service_impl import ProdutoServiceImpl
from services.impl.caixa_service_impl import CaixaServiceImpl  

from controllers.main_app import MainApp
from controllers.autenticacao_controller import AutenticacaoController
from controllers.estoque_controller import EstoqueController
from controllers.funcionario_controller import FuncionarioController
from controllers.pedido_controller import PedidoController
from controllers.produto_controller import ProdutoController
from controllers.caixa_controller import CaixaController  

def main():
    conexaoBancoDeDados = DatabaseConnection()

    # Serviços
    funcionarioService = FuncionarioServiceImpl(conexaoBancoDeDados)
    estoqueService = EstoqueServiceImpl(conexaoBancoDeDados)
    caixaService = CaixaServiceImpl(conexaoBancoDeDados)
    autenticacaoService = AutenticacaoServiceImpl(funcionarioService)
    pedidoService = PedidoServiceImpl(conexaoBancoDeDados)
    produtoService = ProdutoServiceImpl(conexaoBancoDeDados)
    
    # Controllers
    autenticacaoController = AutenticacaoController('autenticacao', autenticacaoService)
    funcionarioController = FuncionarioController('funcionario', funcionarioService, autenticacaoService)
    estoqueController = EstoqueController('estoque', estoqueService, autenticacaoService)
    caixaController = CaixaController('caixa', caixaService, autenticacaoService)
    pedidoController = PedidoController('pedido', pedidoService, autenticacaoService)
    produtoController = ProdutoController('produto', produtoService, autenticacaoService)
    
    controllers = [
        autenticacaoController,
        funcionarioController,
        estoqueController,
        caixaController,
        pedidoController,
        produtoController,
    ]
    
    app = MainApp(controllers)
    app.run()
    
main()
