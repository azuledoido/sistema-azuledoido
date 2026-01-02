import redis
import os
from flask import Flask, render_template

app = Flask(__name__)

# Configura a conexão com o banco de dados Redis
endereco_banco = os.environ.get('BANCO_HOST')
banco = redis.Redis(host=endereco_banco, port=6379, decode_responses=True)

@app.route('/')
def hello():
    try:
        visitas = banco.incr('contador')
        # Adiciona depuração para ver onde ele está procurando
        print(f"DEBUG: Procurando template em: {app.root_path}/templates")
        return render_template('index.html', visitas=visitas)
    except Exception as e:
        return f"Erro ao conectar ao banco de dados: {e}"

# Roda o servidor web na porta que o Render exige
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
