class Estoque:
    def __init__(self, id, nome, quantidade, localizacao, linha, coluna):
        self.id = id
        self.nome = nome
        self.quantidade = quantidade
        self.localizacao = localizacao
        self.posicao = {
            'linha': linha,
            'coluna': coluna
        }
    
    def to_dict(self):
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'quantidade': self.quantidade,
            'localizacao': self.localizacao,
            'posicao': self.posicao
        }

class GerenciadorEstoque:
    def __init__(self, db_connection):
        self.db = db_connection
        print("✅ GerenciadorEstoque instanciado!")
    
    def buscar_todos_itens(self):
        """Busca todos os itens do estoque"""
        print("🔍 Buscando todos os itens no banco...")
        conn = self.db.get_connection()
        if conn is None:
            print("❌ Conexão com banco falhou!")
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM estoque")
            rows = cursor.fetchall()
            print(f"📋 Número de registros no banco: {len(rows)}")
            
            itens = []
            for row in rows:
                item = Estoque(
                    id=row['id'],
                    nome=row['nome'],
                    quantidade=row['quantidade'],
                    localizacao=row['localizacao'],
                    linha=row['linha'],
                    coluna=row['coluna']
                )
                itens.append(item.to_dict())
            
            print(f"✅ Itens convertidos: {len(itens)}")
            return itens
        except Exception as e:
            print(f"❌ Erro ao buscar itens: {e}")
            return []
        finally:
            conn.close()