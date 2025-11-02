from flask import request, jsonify

from classes.contoller_error import ControllerError
from classes.custom_exception import CustomException
from services.produto_service import ProdutoService

class ProdutoController():
    def __init__(self, produto_service: ProdutoService):
        self.produto_service = produto_service
    
    def registrar_rotas(self, app):
        app.add_url_rule('/api/produto', 'adicionar_produto', self.adicionar_produto, methods=['POST'])
        app.add_url_rule('/api/produto', 'editar_produto', self.editar_produto, methods=['PUT'])
        app.add_url_rule('/api/produto/<int:id>', 'remover_produto', self.remover_produto, methods=['DELETE'])
        app.add_url_rule('/api/produto', 'busca_geral_produto', self.busca_geral_produto, methods=['GET'])
        app.add_url_rule('/api/produto/<int:id>', 'busca_produto', self.buscar_produto, methods=['GET'])
        
    def adicionar_produto(self):
        try:
            data = request.get_json()
            required_fields = ['id', 'nome', 'marca', 'preco']
            for field in required_fields:
                if not data.get(field):
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400

            produto = self.produto_service.adicionar_produto(
                id=data['id'],
                nome=data['nome'],
                marca=data['marca'],
                preco=data['preco']
            )
            
            return jsonify({
                'message': 'Produto cadastrado com sucesso',
                'produto': produto.to_dict()
            }), 201
            
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado no cadastro de produto: {e}")
            return jsonify(ControllerError('Erro inesperado ao cadastrar produto').to_dict()), 500
        
    def editar_produto(self):
        try:
            data = request.get_json()
            required_fields = ['id', 'nome', 'marca', 'preco']
            for field in required_fields:
                if not data.get(field):
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400

            produto = self.produto_service.editar_produto(
                id=data['id'],
                nome=data['nome'],
                marca=data['marca'],
                preco=data['preco']
            )
            
            return jsonify({
                'message': 'Produto editado com sucesso',
                'produto': produto.to_dict()
            }), 201
            
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado na edicao de produto: {e}")
            return jsonify(ControllerError('Erro inesperado ao editar produto').to_dict()), 500
    
    def remover_produto(self, id: int):
        try:
            self.produto_service.remover_produto(id)
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao remover de produto com id {id}: {e}")
            return jsonify(ControllerError('Erro inesperado ao remover produto').to_dict()), 500
    
    def busca_geral_produto(self):
        try:
            self.produto_service.busca_geral_produto()
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao buscar produtos: {e}")
            return jsonify(ControllerError('Erro inesperado ao buscar produtos').to_dict()), 500

    def buscar_produto(self, id):
        try:
            self.produto_service.busca_produto(id)
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao buscar produto com id {id}: {e}")
            return jsonify(ControllerError('Erro inesperado ao buscar produto').to_dict()), 500