from flask import Flask, jsonify, request
from flask_cors import CORS
from faker import Faker
import random
import bcrypt

app = Flask(__name__)
CORS(app)

fake = Faker('pt_BR')

def gerar_usuario():
    """Gera usuário fake"""
    senha_plana = fake.password(length=10)
    senha_hash = bcrypt.hashpw(senha_plana.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    return {
        "nome": fake.name(),
        "usuario": fake.unique.user_name(),
        "senha": senha_hash,
        "perfil": random.choice(['primeira', 'regular', 'esporadico', 'voluntario', 'direcionado']),
        "sexo": random.choice(['feminino', 'masculino', 'outro']),
        "sangue": random.choice(['a_positivo', 'a_negativo', 'b_positivo', 'b_negativo', 'ab_positivo', 'ab_negativo', 'o_positivo', 'o_negativo', 'nao_tenho_certeza']),
        "idade": fake.random_int(min=16, max=69)
    }

@app.route("/gerar_usuarios", methods=["POST"])
def gerar_usuarios():
    """Recebe a quantidade e retorna JSON (?) com usuários gerados"""
    try:
        data = request.json() or {}
        qtd = int(data.get("qtd", 5))
        usuarios = [gerar_usuario() for _ in range(qtd)]
        return jsonify({"usuarios": usuarios, "message":f"{qtd} usuários gerados com sucesso."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__== "__main__":
    app.run(port=5001, debug=True)