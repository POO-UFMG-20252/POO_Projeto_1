from database.connection import DatabaseConnection

from services.impl.autenticacao_service_impl import AutenticacaoServiceImpl
from services.impl.estoque_service_impl import EstoqueServiceImpl
from services.impl.funcionario_service_impl import FuncionarioServiceImpl
from services.impl.pedido_service_impl import PedidoServiceImpl
from services.impl.produto_service_impl import ProdutoServiceImpl
from services.impl.venda_service_impl import VendaSeriviceImpl

from controllers.main_app import MainApp
from controllers.autenticacao_controller import AutenticacaoController
from controllers.estoque_controller import EstoqueController
from controllers.funcionario_controller import FuncionarioController
from controllers.pedido_controller import PedidoController
from controllers.produto_controller import ProdutoController
from controllers.venda_controller import VendaController

def main():
    conexaoBancoDeDados = DatabaseConnection()

    funcionarioService = FuncionarioServiceImpl(conexaoBancoDeDados)
    autenticacaoService = AutenticacaoServiceImpl(funcionarioService)
    estoqueService = EstoqueServiceImpl(conexaoBancoDeDados)
    pedidoService = PedidoServiceImpl(conexaoBancoDeDados)
    produtoService = ProdutoServiceImpl(conexaoBancoDeDados)
    vendaService = VendaSeriviceImpl(conexaoBancoDeDados)
    
    autenticacaoController = AutenticacaoController('autenticacao', autenticacaoService)
    funcionarioController = FuncionarioController('funcionario', funcionarioService, autenticacaoService)
    estoqueController = EstoqueController('estoque', estoqueService, autenticacaoService)
    pedidoController = PedidoController('pedido', pedidoService, autenticacaoService)
    produtoController = ProdutoController('produto', produtoService, autenticacaoService)
    
    controllers = [
        autenticacaoController,
        funcionarioController,
        estoqueController,
        pedidoController,
        produtoController,
    ]
    
    app = MainApp(controllers)
    app.run()
    
main()