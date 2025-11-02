# funcionario_controller.py
from flask import Blueprint, request, jsonify
from services.funcionario_service import FuncionarioService
from classes.contoller_error import ControllerError
from classes.custom_exception import CustomException

class FuncionarioController():
    def __init__(self, funcionarioService: FuncionarioService):
        self.funcionarioService = funcionarioService
        
    def registrar_rotas(self, app):
        app.add_url_rule('/funcionarios', 'listar_funcionarios', self.listar_funcionarios, methods=['GET'])
        app.add_url_rule('/funcionarios', 'cadastrar_funcionario', self.cadastrar_funcionario, methods=['POST'])
        
    def listar_funcionarios(self):
        try:
            print("🟡 Recebida requisição para listar funcionários")
            funcionarios = self.funcionarioService.listar_funcionarios()
            print(f"🟢 Retornando {len(funcionarios)} funcionários")
            return jsonify([funcionario.to_dict() for funcionario in funcionarios])
        except CustomException as e:
            print(f"🔴 CustomException: {e}")
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"🔴 Erro inesperado no controller: {e}")
            import traceback
            traceback.print_exc()
            return jsonify(ControllerError('Erro inesperado ao listar funcionários').to_dict()), 500
        
    def cadastrar_funcionario(self):
        try:
            print("🟡 Recebida requisição para cadastrar funcionário")
            data = request.get_json()
            
            # Validações básicas
            required_fields = ['nome', 'cpf', 'email', 'data_nascimento', 'salario', 'tipo']
            for field in required_fields:
                if not data.get(field):
                    return jsonify(ControllerError(f'Campo {field} é obrigatório').to_dict()), 400
            
            # Chamar o service para cadastrar
            funcionario = self.funcionarioService.cadastrar_funcionario(
                nome=data['nome'],
                cpf=data['cpf'],
                email=data['email'],
                data_nascimento=data['data_nascimento'],
                salario=data['salario'],
                tipo=data['tipo']
            )
            
            print(f"🟢 Funcionário cadastrado com sucesso: {funcionario.nome}")
            return jsonify({
                'message': 'Funcionário cadastrado com sucesso',
                'funcionario': funcionario.to_dict()
            }), 201
            
        except CustomException as e:
            print(f"🔴 CustomException no cadastro: {e}")
            return jsonify(ControllerError.de_excecao(e).to_dict()), 400
        except Exception as e:
            print(f"🔴 Erro inesperado no cadastro: {e}")
            import traceback
            traceback.print_exc()
            return jsonify(ControllerError('Erro inesperado ao cadastrar funcionário').to_dict()), 500