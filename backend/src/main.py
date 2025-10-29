from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys

# Adicionar o diretório atual ao path para importações
sys.path.append(os.path.dirname(__file__))

def create_app():
    app = Flask(__name__)
    
    # Configurar CORS
    CORS(app)
    
    # Rota de teste simples
    @app.route('/test')
    def test():
        return jsonify({"message": "Teste OK", "status": "working"})
    
    try:
        from controllers.main_controller import main_bp
        from controllers.estoque_controller import estoque_bp
        from controllers.login_controller import login_bp
        
        app.register_blueprint(main_bp)
        app.register_blueprint(estoque_bp)
        app.register_blueprint(login_bp)
        print("✅ Blueprints registrados com sucesso!")
        
    except ImportError as e:
        print(f"❌ Erro ao importar blueprints: {e}")
    except Exception as e:
        print(f"❌ Erro ao registrar blueprints: {e}")
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Servidor Flask iniciado!")
    print("📊 Endpoints disponíveis:")
    print("   http://localhost:5000/")
    print("   http://localhost:5000/test") 
    print("   http://localhost:5000/api/estoque")
    app.run(debug=True, port=5000)