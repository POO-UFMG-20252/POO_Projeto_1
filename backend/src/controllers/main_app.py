from flask import Flask
from flask_cors import CORS

class MainApp:
    def __init__(self, controllers):
        self.app = Flask(__name__)
        CORS(self.app)  # IMPORTANTE: Adicionar CORS
        
        # Registrar rotas com debug
        print("🎯 Registrando controllers...")
        for controller in controllers:
            print(f"   Registrando: {controller.__class__.__name__}")
            controller.registrar_rotas(self.app)
        
        # Adicionar rota de health check
        @self.app.route('/health')
        def health():
            return jsonify({"status": "ok", "message": "API está funcionando"})
        
        @self.app.route('/')
        def home():
            return jsonify({"message": "API Flask funcionando!"})

    def run(self):
        print("🌟 Iniciando servidor na porta 5000...")
        self.app.run(debug=True, host='0.0.0.0', port=5000)