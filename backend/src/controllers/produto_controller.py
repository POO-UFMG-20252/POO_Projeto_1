from flask import request, jsonify

from classes.contoller_error import ControllerError
from classes.custom_exception import CustomException
from controllers.controller import Controller
from services.autenticacao_service import AutenticacaoService
from services.produto_service import ProdutoService

class ProdutoController(Controller):
    def __init__(self, nome: str, produto_service: ProdutoService, autenticacaoService: AutenticacaoService):
        super().__init__(nome, autenticacaoService)
        self.produto_service = produto_service
    
    def registrar_rotas(self, app):
        app.add_url_rule('/api/produto', 'adicionar_produto', self.adicionar_produto, methods=['POST'])
        app.add_url_rule('/api/produto', 'editar_produto', self.editar_produto, methods=['PUT'])
        app.add_url_rule('/api/produto/<int:id>', 'remover_produto', self.remover_produto, methods=['DELETE'])
        app.add_url_rule('/api/produto', 'busca_geral_produto', self.busca_geral_produto, methods=['GET'])
        app.add_url_rule('/api/produto/<int:id>', 'busca_produto', self.buscar_produto, methods=['GET'])
        app.add_url_rule('/api/produto/buscar', 'busca_produto_por_nome', self.buscar_produto_por_nome, methods=['GET'])
        
    def adicionar_produto(self):
        try:
            usuario = self._get_usuario_logado(request, [0, 1, 2])
            
            data = request.get_json()
            required_fields = ['nome', 'marca', 'preco']
            for field in required_fields:
                if not data.get(field):
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400

            produto = self.produto_service.adicionar_produto(
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
            usuario = self._get_usuario_logado(request, [0, 1, 2])
            
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
            usuario = self._get_usuario_logado(request, [0, 1, 2])
            
            if not id:
                raise(CustomException("Id inválido"))
            
            jsonify(self.produto_service.remover_produto(id).to_dict()), 200
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao remover de produto com id {id}: {e}")
            return jsonify(ControllerError('Erro inesperado ao remover produto').to_dict()), 500
    
    def busca_geral_produto(self):
        try:
            usuario = self._get_usuario_logado(request, [0, 1, 2])
            
            return jsonify(self.produto_service.busca_geral_produto()), 200
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao buscar produtos: {e}")
            return jsonify(ControllerError('Erro inesperado ao buscar produtos').to_dict()), 500

    def buscar_produto(self, id):
        try:
            usuario = self._get_usuario_logado(request, [0, 1, 2])
            
            if not id:
                raise(CustomException("Id inválido"))

            return jsonify(self.produto_service.busca_produto(id).to_dict()), 200
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao buscar produto com id {id}: {e}")
            return jsonify(ControllerError('Erro inesperado ao buscar produto').to_dict()), 500
        
    def buscar_produto_por_nome(self):
        try:
            usuario = self._get_usuario_logado(request, [0, 1, 2])
            
            if not usuario:
                return jsonify(ControllerError('Usuário não autenticado').to_dict()), 401
            
            termo = request.args.get('q', '')
            
            if not termo or len(termo.strip()) < 2:
                return jsonify([])
            
            produtos = self.produto_service.buscar_produtos_por_nome(termo.strip())
            
            return jsonify([produto.to_dict() for produto in produtos])
            
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao buscar produtos por nome: {e}")
            return jsonify(ControllerError('Erro inesperado ao buscar produtos').to_dict()), 500