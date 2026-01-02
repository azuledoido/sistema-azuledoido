import redis
import os
from flask import Flask
import logging

# Configurações de log para o Render
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# CONFIGURAÇÃO INTELIGENTE DO REDIS:
# No Render, ele usará a 'REDIS_URL'. No seu PC, usará o host 'db'.
redis_url = os.environ.get('REDIS_URL', 'redis://db:6379')

try:
    # Conecta usando a URL completa (mais seguro para nuvem)
    banco = redis.Redis.from_url(redis_url, decode_responses=True)
except Exception as e:
    logging.error(f"Falha na configuração inicial do Redis: {e}")

@app.route('/')
def hello():
    try:
        visitas = banco.incr('contador')
    except Exception as e:
        app.logger.error(f"Erro ao conectar ao Redis: {e}")
        visitas = "Indisponível (Erro no Banco)"

    # Seu portfólio completo com o visual que você gosta
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Portfólio Técnico - Azuledoido</title>
        <style>
            body {{ font-family: sans-serif; background-color: #eef2f7; text-align: center; padding: 50px; }}
            .container {{ max-width: 700px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-top: 10px solid #0047ab; }}
            h1 {{ color: #0047ab; }}
            .metrics {{ background: #f0f0f0; padding: 10px; border-radius: 8px; margin: 20px 0; border: 1px dashed #0047ab; }}
            .destaque {{ color: #d00000; font-weight: bold; }}
            a {{ color: #0047ab; text-decoration: none; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Olá, eu sou Azuledoido!</h1>
            <p>Este é o meu <strong>portfólio técnico</strong>. Tudo aqui roda em <strong>Docker, Flask e Redis</strong>.</p>
            <p class="destaque">Seus projetos estarão seguros em um ambiente moderno e automatizado.</p>
            
            <div class="metrics">
                <h3>Métricas do Site:</h3>
                <p>Este site foi visitado <strong>{visitas}</strong> vezes.</p>
            </div>

            <p>Entre em contato: <strong>azuledoido@gmail.com</strong></p>
            <p><small>SISTEMA AZULEDOIDO 2026</small></p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    # O Render usa a porta 10000 por padrão, mas o código aceita qualquer uma
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
