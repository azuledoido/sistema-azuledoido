import redis
import os
from flask import Flask
import logging
from datetime import datetime

# Configurações de log para o Render
logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# CONFIGURAÇÃO DO REDIS
redis_url = os.environ.get('REDIS_URL', 'redis://db:6379')

try:
    banco = redis.Redis.from_url(redis_url, decode_responses=True)
except Exception as e:
    logging.error(f"Falha na configuração inicial do Redis: {e}")

@app.route('/')
def hello():
    try:
        # Lógica do Contador e do Log de Tempo
        visitas = banco.incr('contador')
        
        horario_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        banco.lpush('historico_visitas', horario_atual) 
        banco.ltrim('historico_visitas', 0, 4)
        
        # Pega o horário da visita anterior
        anterior = banco.lindex('historico_visitas', 1) or "Primeiro acesso!"
        
    except Exception as e:
        app.logger.error(f"Erro ao conectar ao Redis: {e}")
        visitas = "Indisponível"
        anterior = "Erro no Banco"

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
            }}
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
