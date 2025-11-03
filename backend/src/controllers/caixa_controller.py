from flask import request, jsonify
from services.autenticacao_service import AutenticacaoService
from controllers.controller import Controller
from services.caixa_service import CaixaService
from classes.contoller_error import ControllerError
from classes.custom_exception import CustomException

class CaixaController(Controller):
    def __init__(self, nome: str, caixaService: CaixaService, autenticacaoService: AutenticacaoService):
        super().__init__(nome, autenticacaoService)
        self.caixaService = caixaService
        
    def registrar_rotas(self, app):
        app.add_url_rule('/api/caixa/venda/processar', 'processar_venda', self.processar_venda, methods=['POST'])
    
    def processar_venda(self):
        try:
            usuario = super()._get_usuario_logado(request, [0, 1])

            usuario = self.auth_utils.get_usuario_logado()
            if not usuario:
                return jsonify(ControllerError('Usuário não autenticado').to_dict()), 401
            
            data = request.get_json()
            
            # Validar dados obrigatórios
            if not data or 'itens' not in data:
                return jsonify(ControllerError('Lista de itens é obrigatória').to_dict()), 400
            
            itens_venda = data['itens']
            id_operador = usuario.get('id') or 1  # Usar ID do usuário logado ou default
            
            if not isinstance(itens_venda, list) or len(itens_venda) == 0:
                return jsonify(ControllerError('Lista de itens não pode estar vazia').to_dict()), 400
            
            # Validar cada item
            for item in itens_venda:
                required_fields = ['id', 'nome', 'preco', 'quantidade']
                for field in required_fields:
                    if field not in item:
                        return jsonify(ControllerError(f'Campo {field} é obrigatório em todos os itens').to_dict()), 400
                
                if item['quantidade'] <= 0:
                    return jsonify(ControllerError('Quantidade deve ser maior que zero').to_dict()), 400
            
            resultado = self.caixaService.processar_venda(itens_venda, id_operador)
            
            return jsonify(resultado)
            
        except CustomException as e:
            print(f"CustomException: {e}")
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
            return jsonify(ControllerError('Erro inesperado ao processar venda').to_dict()), 500