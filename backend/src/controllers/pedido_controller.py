from flask import request, jsonify
from services.pedido_service import PedidoService
from services.autenticacao_service import AutenticacaoService
from controllers.controller import Controller
from classes.contoller_error import ControllerError
from classes.custom_exception import CustomException

class PedidoController(Controller):
    def __init__(self, nome: str, pedidoService: PedidoService, autenticacaoService: AutenticacaoService):
        super().__init__(nome, autenticacaoService)
        self.__pedido_service = pedidoService
        
    def registrar_rotas(self, app):
        app.add_url_rule('/api/pedido', 'adicionar_pedido', self.adicionar_pedido, methods=['POST'])
        app.add_url_rule('/api/pedido/<int:id>', 'editar_pedido', self.editar_pedido, methods=['PUT'])
        app.add_url_rule('/api/pedido/<int:id>', 'remover_pedido', self.remover_pedido, methods=['DELETE'])
        app.add_url_rule('/api/pedido/<int:id>', 'buscar_pedido', self.buscar_pedido, methods=['GET'])
        app.add_url_rule('/api/pedidos', 'listar_pedidos', self.listar_pedidos, methods=['GET'])
        app.add_url_rule('/api/pedido/<int:id>/estado', 'alterar_estado_pedido', self.alterar_estado_pedido, methods=['PUT'])
        
    def adicionar_pedido(self):
        try:
            usuario_logado = super()._get_usuario_logado(request, [0, 1, 2])  # Todos os tipos podem fazer pedidos
            
            # CORREÇÃO: Verificar se é dicionário e extrair o CPF
            if isinstance(usuario_logado, dict):
                id_responsavel = usuario_logado.get('cpf')
            else:
                id_responsavel = usuario_logado.cpf
                
            if not id_responsavel:
                return jsonify(ControllerError('Usuário não autenticado').to_dict()), 401

            data = request.get_json()
            
            # Validações
            required_fields = ['lista_produtos']
            for field in required_fields:
                if not data.get(field):
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400
            
            lista_produtos = data['lista_produtos']
            if not isinstance(lista_produtos, list) or len(lista_produtos) == 0:
                return jsonify(ControllerError('Lista de produtos deve conter pelo menos um produto').to_dict()), 400
            
            # Validar cada produto
            for produto in lista_produtos:
                if len(produto) != 4:
                    return jsonify(ControllerError('Cada produto deve ter [nome, marca, preco, quantidade]').to_dict()), 400
                
                nome, marca, preco, quantidade = produto
                
                if not nome or not marca:
                    return jsonify(ControllerError('Nome e marca são obrigatórios para cada produto').to_dict()), 400
                
                if float(preco) <= 0:
                    return jsonify(ControllerError('Preço deve ser maior que zero').to_dict()), 400
                
                if int(quantidade) <= 0:
                    return jsonify(ControllerError('Quantidade deve ser maior que zero').to_dict()), 400
            
            # Criar pedido
            pedido = self.__pedido_service.adicionar_pedido(
                id_responsavel=id_responsavel,  # USAR A VARIÁVEL CORRIGIDA
                estado=0,  # Estado inicial: Pendente
                lista_produtos=lista_produtos
            )
            
            return jsonify({
                'message': 'Pedido criado com sucesso',
                'pedido': pedido.to_dict()
            }), 201
            
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao criar pedido: {e}")
            return jsonify(ControllerError('Erro inesperado ao criar pedido').to_dict()), 500
    
    def editar_pedido(self, id: int):
        try:
            super()._get_usuario_logado(request, [0, 1])  # Apenas Gerente e Repositor podem editar
            
            data = request.get_json()
            
            if not data.get('estado'):
                return jsonify(ControllerError('Campo estado é obrigatório').to_dict()), 400
            
            estado = data['estado']
            if estado not in [0, 1, 2]:  # 0=Pendente, 1=Processando, 2=Concluído
                return jsonify(ControllerError('Estado inválido').to_dict()), 400
            
            pedido = self.__pedido_service.editar_pedido(id, estado)
            
            return jsonify({
                'message': 'Pedido atualizado com sucesso',
                'pedido': pedido.to_dict()
            }), 200
            
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao editar pedido: {e}")
            return jsonify(ControllerError('Erro inesperado ao editar pedido').to_dict()), 500
    
    def remover_pedido(self, id: int):
        try:
            super()._get_usuario_logado(request, [0])  # Apenas Gerente pode remover
            
            pedido = self.__pedido_service.remover_pedido(id)
            
            return jsonify({
                'message': 'Pedido removido com sucesso',
                'pedido': pedido.to_dict()
            }), 200
            
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao remover pedido: {e}")
            return jsonify(ControllerError('Erro inesperado ao remover pedido').to_dict()), 500
    
    def buscar_pedido(self, id: int):
        try:
            super()._get_usuario_logado(request, [0, 1, 2])  # Todos podem buscar
            
            pedido = self.__pedido_service.buscar_pedido(id)
            
            if not pedido:
                return jsonify(ControllerError('Pedido não encontrado').to_dict()), 404
            
            return jsonify(pedido.to_dict()), 200
            
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao buscar pedido: {e}")
            return jsonify(ControllerError('Erro inesperado ao buscar pedido').to_dict()), 500
        
    def listar_pedidos(self):
        try:
            super()._get_usuario_logado(request, [0, 1, 2])  # Todos podem visualizar pedidos

            pedidos = self.__pedido_service.listar_pedidos()

            # Converter para dicionário com estado_texto para o frontend
            pedidos_dict = []
            for pedido in pedidos:
                pedido_dict = pedido.to_dict()
                # Adicionar estado_texto para o frontend
                pedido_dict['estado_texto'] = self._converter_estado_texto(pedido.estado)
                pedidos_dict.append(pedido_dict)

            return jsonify(pedidos_dict), 200

        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao listar pedidos: {e}")
            return jsonify(ControllerError('Erro inesperado ao listar pedidos').to_dict()), 500
        
    def alterar_estado_pedido(self, id: int):
        try:
            super()._get_usuario_logado(request, [0, 1])  # Apenas Gerente e Repositor podem alterar estado
            
            data = request.get_json()
            
            if not data or 'novo_estado' not in data:
                return jsonify(ControllerError('Campo novo_estado é obrigatório').to_dict()), 400
            
            novo_estado = data['novo_estado']
            
            # Validar o estado
            if novo_estado not in [0, 1, 2, 3]:
                return jsonify(ControllerError('Estado inválido. Use: 0=Aguardando, 1=A caminho, 2=Entregue, 3=Finalizado').to_dict()), 400
            
            # Alterar o estado do pedido
            pedido_atualizado = self.__pedido_service.alterar_estado_pedido(id, novo_estado)
            
            pedido_dict = pedido_atualizado.to_dict()
            pedido_dict['estado_texto'] = self._converter_estado_texto(pedido_atualizado.estado)
            
            return jsonify({
                'message': f'Estado do pedido alterado para {pedido_dict["estado_texto"]}',
                'pedido': pedido_dict
            }), 200
            
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao alterar estado do pedido: {e}")
            return jsonify(ControllerError('Erro inesperado ao alterar estado do pedido').to_dict()), 500

    def _converter_estado_texto(self, estado: int) -> str:
        estados = {
            0: 'Aguardando',
            1: 'A caminho', 
            2: 'Entregue',
            3: 'Finalizado'
        }
        return estados.get(estado, 'Desconhecido')