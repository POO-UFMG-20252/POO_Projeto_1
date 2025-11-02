from flask import Blueprint, jsonify
import os
import sys

# Adicionar path para importações
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from database.connection import DatabaseConnection
from classes.estoque import GerenciadorEstoque

estoque_bp = Blueprint('estoque', __name__)

print("🔄 Inicializando controlador de estoque...")

try:
    db_connection = DatabaseConnection()
    gerenciador_estoque = GerenciadorEstoque(db_connection)
    print("✅ Gerenciador de estoque inicializado!")
except Exception as e:
    print(f"❌ Erro ao inicializar gerenciador: {e}")

@estoque_bp.route('/api/estoque', methods=['GET'])
def get_estoque():
    """Retorna todos os itens do estoque"""
    print("📥 Recebida requisição para /api/estoque")
    try:
        itens = gerenciador_estoque.buscar_todos_itens()
        print(f"📊 Itens encontrados: {len(itens)}")
        return jsonify(itens)
    except Exception as e:
        print(f"❌ Erro em /api/estoque: {e}")
        return jsonify({'error': str(e)}), 500

@estoque_bp.route('/api/estoque/<int:item_id>', methods=['GET'])
def get_item_estoque(item_id):
    """Retorna um item específico do estoque"""
    try:
        item = gerenciador_estoque.buscar_item_por_id(item_id)
        if item:
            return jsonify(item)
        return jsonify({'error': 'Item não encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500