from flask import Blueprint, request, jsonify
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.connection import DatabaseConnection

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    cpf = data.get('cpf')
    senha = data.get('senha')

    if not cpf or not senha:
        return jsonify({'message': 'CPF e senha são obrigatórios'}), 400

    try:
        db = DatabaseConnection()
        conn = db.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE cpf = ?", (cpf,))
        user = cursor.fetchone()

        if not user:
            return jsonify({'message': 'Usuário não encontrado'}), 404

        if senha != user['senha']:
            return jsonify({'message': 'Senha incorreta'}), 401

        usuario_data = {
            'id': user['id'],
            'nome': user['nome'],
            'cpf': user['cpf']
        }

        # Simulando geração de token (em produção, use JWT)
        token = "fake-token-123"

        return jsonify({'usuario': usuario_data, 'token': token}), 200

    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return jsonify({'message': 'Erro interno no servidor'}), 500
