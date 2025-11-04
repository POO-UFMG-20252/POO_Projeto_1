from flask import Blueprint, request, jsonify
from services.autenticacao_service import AutenticacaoService
from services.estoque_service import EstoqueService
from classes.contoller_error import ControllerError
from classes.custom_exception import CustomException
from controllers.controller import Controller

class EstoqueController(Controller):
    def __init__(self, nome: str, estoqueService: EstoqueService, autenticacaoService: AutenticacaoService):
        super().__init__(nome, autenticacaoService)
        self.estoqueService = estoqueService
        
    def registrar_rotas(self, app):
        app.add_url_rule('/api/estoque/visualizacao', 'obter_visualizacao_estoque', self.obter_visualizacao_estoque, methods=['GET'])
        app.add_url_rule('/api/estoque/mover', 'mover_produto', self.mover_produto, methods=['POST'])
        app.add_url_rule('/api/estoque/adicionar', 'adicionar_produto_no_estoque', self.adicionar_produto_no_estoque, methods=['POST'])
        app.add_url_rule('/api/estoque/remover/<int:id_item>', 'remover_produto_do_estoque', self.remover_produto_do_estoque, methods=['DELETE'])
        app.add_url_rule('/api/estoque/produtos', 'listar_produtos_do_estoque', self.listar_produtos_do_estoque, methods=['GET'])
        
    def obter_visualizacao_estoque(self):
        try:
            usuario = super()._get_usuario_logado(request, [0, 1, 2])
            
            dados_estoque = self.estoqueService.obter_visualizacao_estoque()
            return jsonify(dados_estoque)
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado: {e}")
            import traceback
            traceback.print_exc()
            return jsonify(ControllerError('Erro inesperado ao carregar estoque').to_dict()), 500
    
    def mover_produto(self):
        try:
            usuario = super()._get_usuario_logado(request, [0, 1, 2])      

            data = request.get_json()
            required_fields = ['id_item', 'novo_pos_x', 'novo_pos_y', 'novo_local']
            for field in required_fields:
                if field not in data:
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400
            
            sucesso = self.estoqueService.mover_produto(
                data['id_item'],
                data['novo_pos_x'],
                data['novo_pos_y'],
                data['novo_local']
            )
            
            if sucesso:
                return jsonify({'message': 'Produto movido com sucesso'})
            else:
                return jsonify(ControllerError('Erro ao mover produto').to_dict()), 400
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro ao mover produto: {e}")
            return jsonify(ControllerError('Erro inesperado ao mover produto').to_dict()), 500
    
    def adicionar_produto_no_estoque(self):
        try:
            usuario = super()._get_usuario_logado(request, [0, 1, 2])
            
            data = request.get_json()
            required_fields = ['id_produto', 'pos_x', 'pos_y', 'quantidade', 'local']
            for field in required_fields:
                if field not in data:
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400
            
            sucesso = self.estoqueService.adicionar_produto(
                data['id_produto'],
                data['pos_x'],
                data['pos_y'],
                data['quantidade'],
                data['local']
            )
            
            if sucesso:
                return jsonify({'message': 'Produto adicionado com sucesso'})
            else:
                return jsonify(ControllerError('Erro ao adicionar produto').to_dict()), 400
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro ao adicionar produto: {e}")
            return jsonify(ControllerError('Erro inesperado ao adicionar produto').to_dict()), 500
    
    def remover_produto_do_estoque(self, id_item):
        try:
            usuario = super()._get_usuario_logado(request, [0, 1, 2])            
            
            sucesso = self.estoqueService.remover_produto(id_item)
            
            if sucesso:
                return jsonify({'message': 'Produto removido com sucesso'})
            else:
                return jsonify(ControllerError('Produto não encontrado').to_dict()), 404
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro ao remover produto: {e}")
            return jsonify(ControllerError('Erro inesperado ao remover produto').to_dict()), 500
    
    def listar_produtos_do_estoque(self):
        try:
            usuario = super()._get_usuario_logado(request, [0, 1, 2])
            
            produtos = self.estoqueService.listar_produtos()
            return jsonify([produto.to_dict() for produto in produtos])
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro ao listar produtos: {e}")
            return jsonify(ControllerError('Erro inesperado ao listar produtos').to_dict()), 500
