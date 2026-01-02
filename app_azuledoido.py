import redis
import time
import os

# Forçamos o uso da variável de ambiente que configuramos no Render
endereco_banco = os.environ.get('BANCO_HOST')

try:
    banco = redis.Redis(host=endereco_banco, port=6379, decode_responses=True)
    print("--- SISTEMA AZULEDOIDO 2026 ---")
    visitas = banco.incr('contador')
    print(f"Sucesso! Acesso número: {visitas}")
except Exception as e:
    print(f"Erro: {e}")

time.sleep(3600)
