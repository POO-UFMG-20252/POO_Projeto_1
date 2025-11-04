# funcionario_controller.py
from flask import request, jsonify

from services.funcionario_service import FuncionarioService
from services.autenticacao_service import AutenticacaoService
from controllers.controller import Controller
from classes.contoller_error import ControllerError
from classes.custom_exception import CustomException

class FuncionarioController(Controller):
    def __init__(self, nome: str, funcionarioService: FuncionarioService, autenticacaoService: AutenticacaoService):
        super().__init__(nome, autenticacaoService)
        self.__funcionario_service = funcionarioService
        
    def registrar_rotas(self, app):
        app.add_url_rule('/api/funcionarios', 'listar_funcionarios', self.listar_funcionarios, methods=['GET'])
        app.add_url_rule('/api/funcionarios', 'cadastrar_funcionario', self.cadastrar_funcionario, methods=['POST'])
        app.add_url_rule('/api/funcionarios', 'demitir_funcionario', self.demitir_funcionario, methods=['PUT'])
        app.add_url_rule('/api/funcionarios/ponto', 'bater_ponto', self.bater_ponto, methods=['POST'])
        
    def listar_funcionarios(self):        
        try:            
            super()._get_usuario_logado(request, [0])
            
            funcionarios = self.__funcionario_service.listar_funcionarios()
            return jsonify([funcionario.to_dict() for funcionario in funcionarios])
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado no ao listar funcionarios: {e}")
            return jsonify(ControllerError('Erro inesperado ao listar funcionários').to_dict()), 500
        
    def cadastrar_funcionario(self):
        try:
            super()._get_usuario_logado(request, [0])
            
            data = request.get_json()
            
            # Validações básicas
            required_fields = ['nome', 'cpf', 'email', 'senha', 'data_nascimento', 'salario', 'tipo']
            for field in required_fields:
                if not data.get(field):
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400
            
            # Chamar o service para cadastrar
            funcionario = self.__funcionario_service.cadastrar_funcionario(
                nome=data['nome'],
                cpf=data['cpf'],
                email=data['email'],
                senha=data['senha'],
                data_nascimento=data['data_nascimento'],
                salario=data['salario'],
                tipo=data['tipo']
            )
            
            return jsonify({
                'message': 'Funcionário cadastrado com sucesso',
                'funcionario': funcionario.to_dict()
            }), 201
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado no cadastro de funcionario: {e}")
            return jsonify(ControllerError('Erro inesperado ao cadastrar funcionário').to_dict()), 500
        
    def demitir_funcionario(self):
        try:
            super()._get_usuario_logado(request, [0])
            
            data = request.get_json()
            
            # Validações básicas
            required_fields = ['cpf', 'motivo']
            for field in required_fields:
                if not data.get(field):
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400
            
            return self.__funcionario_service.demitir(data.get('cpf'), data.get('motivo'))
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao demitir funcionario: {e}")
            return jsonify(ControllerError('Erro inesperado ao demitir funcionario').to_dict()), 500
        
    def bater_ponto(self):
        try:
            # Permitir que qualquer funcionário logado bata ponto (tipos 0, 1, 2)
            usuario_logado = super()._get_usuario_logado(request, [0, 1, 2])
            
            data = request.get_json()
            
            # Validações básicas
            required_fields = ['tipo']
            for field in required_fields:
                if not data.get(field) and data.get(field) != 0:
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400
            
            tipo = data.get('tipo')
            if tipo not in [0, 1]:
                return jsonify(ControllerError('Tipo de ponto inválido (0=Entrada, 1=Saída)').to_dict()), 400
            
            # Usar CPF do usuário logado
            cpf_funcionario = usuario_logado['cpf']
            
            resultado = self.__funcionario_service.bater_ponto(cpf_funcionario, tipo)
            
            return jsonify({
                'message': resultado['mensagem'],
                'ponto': resultado
            }), 201
            
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado ao bater ponto: {e}")
            return jsonify(ControllerError('Erro inesperado ao bater ponto').to_dict()), 500
