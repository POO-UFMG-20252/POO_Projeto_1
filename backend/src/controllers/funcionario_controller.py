# funcionario_controller.py
from flask import request, jsonify
from services.funcionario_service import FuncionarioService
from services.autenticacao_service import AutenticacaoService
from classes.contoller_error import ControllerError
from classes.custom_exception import CustomException

class FuncionarioController():
    def __init__(self, funcionarioService: FuncionarioService):
        self.funcionario_service = funcionarioService
        
    def registrar_rotas(self, app):
        app.add_url_rule('/api/funcionarios', 'listar_funcionarios', self.listar_funcionarios, methods=['GET'])
        app.add_url_rule('/api/funcionarios', 'cadastrar_funcionario', self.cadastrar_funcionario, methods=['POST'])
        
    def listar_funcionarios(self):        
        try:            
            funcionarios = self.funcionario_service.listar_funcionarios()
            return jsonify([funcionario.to_dict() for funcionario in funcionarios])
        except CustomException as e:
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"Erro inesperado no ao listar funcionarios: {e}")
            return jsonify(ControllerError('Erro inesperado ao listar funcionários').to_dict()), 500
        
    def cadastrar_funcionario(self):
        try:
            data = request.get_json()
            
            # Validações básicas
            required_fields = ['nome', 'cpf', 'email', 'senha', 'data_nascimento', 'salario', 'tipo']
            for field in required_fields:
                if not data.get(field):
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400
            
            # Chamar o service para cadastrar
            funcionario = self.funcionario_service.cadastrar_funcionario(
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