import redis
import os
from flask import Flask
import logging

# Configurações de log para o Render
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# CONFIGURAÇÃO INTELIGENTE DO REDIS:
# No Render, ele usará a 'REDIS_URL'. No seu PC (Zorin), usará o host 'db'.
redis_url = os.environ.get('REDIS_URL', 'redis://db:6379')

try:
    # Conecta usando a URL completa (mais seguro para nuvem/Valkey)
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

    # Seu portfólio completo com o NOVO VISUAL AZUL TECH
    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Portfólio Técnico - Azuledoido</title>
        <style>
            :root {{
                --azul-deep: #003366;
                --azul-tech: #007bff;
                --bg-light: #f4f7f9;
            }}
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%); 
                color: #333;
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
            }}
            .container {{ 
                max-width: 600px; 
                width: 90%;
                background: white; 
                padding: 40px; 
                border-radius: 20px; 
                box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
                border-top: 8px solid var(--azul-tech);
                text-align: center;
                transition: transform 0.3s ease;
            }}
            .container:hover {{
                transform: translateY(-5px);
            }}
            h1 {{ color: var(--azul-deep); margin-top: 0; }}
            .status-badge {{
                display: inline-block;
                background: #d4edda;
                color: #155724;
                padding: 5px 15px;
                border-radius: 50px;
                font-size: 0.8em;
                font-weight: bold;
                margin-bottom: 20px;
            }}
            .metrics {{ 
                background: #f8f9fa; 
                padding: 20px; 
                border-radius: 12px; 
                margin: 25px 0; 
                border-left: 5px solid var(--azul-tech);
            }}
            .metrics h3 {{ margin: 0; color: var(--azul-tech); font-size: 1em; text-transform: uppercase; }}
            .contador {{ font-size: 2.5em; font-weight: bold; color: var(--azul-deep); display: block; margin: 10px 0; }}
            .destaque {{ color: #555; line-height: 1.6; font-size: 1.1em; }}
            .footer {{ margin-top: 30px; font-size: 0.85em; color: #888; border-top: 1px solid #eee; padding-top: 15px; }}
            strong {{ color: var(--azul-tech); }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="status-badge">● Sistema Online</div>
            <h1>Olá, eu sou Azuledoido!</h1>
            <p class="destaque">Este é o meu <strong>portfólio técnico</strong> de 2026. <br> 
            Ambiente totalmente automatizado com <strong>Docker</strong> e <strong>Flask</strong>.</p>
            
            <div class="metrics">
                <h3>Acessos ao Portfólio</h3>
                <span class="contador">{visitas}</span>
                <p><small>Dados processados em tempo real pelo Redis</small></p>
            </div>

            <p>Contato profissional: <strong>azuledoido@gmail.com</strong></p>
            
            <div class="footer">
                SISTEMA AZULEDOIDO &copy; 2026 - Desenvolvido em Zorin OS 18
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    # O Render define a porta automaticamente na variável PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
