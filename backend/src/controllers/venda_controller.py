from flask import request, jsonify

from classes.custom_exception import CustomException
from classes.contoller_error import ControllerError
from controllers.controller import Controller
from services.venda_service import VendaService
from services.autenticacao_service import AutenticacaoService

class VendaController(Controller):
    def __init__(self, nome: str, vendaService: VendaService, autenticacaoService: AutenticacaoService):
        super().__init__(nome, autenticacaoService)
        self.venda_service = vendaService
    
    def registrar_rotas(self, app):
        app.add_url_rule('/api/vendas', 'registrar_venda', self.registar_venda, methods=['POST'])
        
    def registrar_vendas(self):
        try:
            data = request.get_json()
            
            # Validações básicas
            required_fields = ['id_responsavel', 'lista_venda', 'id_mercado']
            for field in required_fields:
                if not data.get(field):
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400

            return self.venda_service.registrar_venda(
				id_responsavel=data['id_responsavel'],
				lista_venda=data['lista_venda'],
				id_mercado=data['id_mercado']
			)        
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado no cadastro de venda: {e}")
            return jsonify(ControllerError('Erro inesperado ao cadastrar venda').to_dict()), 500