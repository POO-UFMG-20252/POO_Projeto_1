from flask import Blueprint, request, jsonify
from services.caixa_service import CaixaService
from classes.contoller_error import ControllerError
from classes.custom_exception import CustomException
from utils.helpers import AuthUtils

class CaixaController():
    def __init__(self, caixaService: CaixaService):
        self.caixaService = caixaService
        self.auth_utils = AuthUtils()
        
    def registrar_rotas(self, app):
        app.add_url_rule('/api/caixa/produtos/buscar', 'buscar_produtos', self.buscar_produtos, methods=['GET'])
        app.add_url_rule('/api/caixa/venda/processar', 'processar_venda', self.processar_venda, methods=['POST'])
        app.add_url_rule('/api/caixa/produtos/<int:id_produto>', 'obter_produto', self.obter_produto, methods=['GET'])
        
    def buscar_produtos(self):
        try:
            usuario = self.auth_utils.get_usuario_logado()
            if not usuario:
                return jsonify(ControllerError('Usuário não autenticado').to_dict()), 401
            
            termo = request.args.get('q', '')
            
            if not termo or len(termo.strip()) < 2:
                return jsonify([])
            
            print(f"🔍 Buscando produtos com termo: '{termo}'")
            produtos = self.caixaService.buscar_produtos_por_nome(termo.strip())
            print(f"Encontrados {len(produtos)} produtos")
            
            return jsonify([produto.to_dict() for produto in produtos])
            
        except CustomException as e:
            print(f"CustomException: {e}")
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
            return jsonify(ControllerError('Erro inesperado ao buscar produtos').to_dict()), 500
    
    def processar_venda(self):
        try:
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
            
            print(f"Processando venda com {len(itens_venda)} itens")
            resultado = self.caixaService.processar_venda(itens_venda, id_operador)
            print(f"Venda processada com sucesso: {resultado}")
            
            return jsonify(resultado)
            
        except CustomException as e:
            print(f"CustomException: {e}")
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
            return jsonify(ControllerError('Erro inesperado ao processar venda').to_dict()), 500
    
    def obter_produto(self, id_produto):
        try:
            usuario = self.auth_utils.get_usuario_logado()
            if not usuario:
                return jsonify(ControllerError('Usuário não autenticado').to_dict()), 401
            
            produto = self.caixaService.obter_produto_por_id(id_produto)
            return jsonify(produto.to_dict())
            
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 404
        except Exception as e:
            print(f"Erro ao obter produto: {e}")
            return jsonify(ControllerError('Erro inesperado ao obter produto').to_dict()), 500