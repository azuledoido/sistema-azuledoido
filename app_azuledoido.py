import redis
import os
from flask import Flask
import logging
from datetime import datetime  # <--- NOVA IMPORTAÇÃO

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

redis_url = os.environ.get('REDIS_URL', 'redis://db:6379')

try:
    banco = redis.Redis.from_url(redis_url, decode_responses=True)
except Exception as e:
    logging.error(f"Falha na configuração inicial do Redis: {e}")

@app.route('/')
def hello():
    try:
        # Soma a visita
        visitas = banco.incr('contador')
        
        # --- NOVO: GUARDA O HORÁRIO DA ÚLTIMA VISITA ---
        horario_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        banco.lpush('historico_visitas', horario_atual) 
        banco.ltrim('historico_visitas', 0, 4) # Guarda apenas as últimas 5 visitas
        # ----------------------------------------------
        
        ultima_visita = banco.lindex('historico_visitas', 1) or "Primeira visita!"
        
    except Exception as e:
        app.logger.error(f"Erro ao conectar ao Redis: {e}")
        visitas = "Indisponível"
        ultima_visita = "Erro no Log"

    return f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Portfólio Técnico - Azuledoido</title>
        <style>
            :root {{ --azul-deep: #003366; --azul-tech: #007bff; }}
            body {{ 
                font-family: 'Segoe UI', sans-serif; 
                background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%); 
                display: flex; align-items: center; justify-content: center; 
                min-height: 100vh; margin: 0; 
            }}
            .container {{ 
                max-width: 600px; width: 90%; background: white; 
                padding: 40px; border-radius: 20px; text-align: center;
                box-shadow: 0 15px 35px rgba(0,0,0,0.1); border-top: 8px solid var(--azul-tech);
            }}
            .metrics {{ background: #f8f9fa; padding: 20px; border-radius: 12px; margin: 20px 0; }}
            .contador {{ font-size: 2.5em; font-weight: bold; color: var(--azul-deep); }}
            .log {{ font-size: 0.85em; color: #666; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Olá, eu sou Azuledoido!</h1>
            <p>Este é o meu portfólio técnico. Tudo aqui roda em <strong>Docker, Flask e Redis</strong>.</p>
            
            <div class="metrics">
                <h3>Acessos ao Portfólio</h3>
                <span class="contador">{visitas}</span>
                <p class="log">Acesso anterior: <strong>{ultima_visita}</strong></p>
            </div>

            <p>Contato: <strong>azuledoido@gmail.com</strong></p>
            <div style="font-size: 0.8em; color: #888; margin-top: 20px;">
                SISTEMA AZULEDOIDO &copy; 2026
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
