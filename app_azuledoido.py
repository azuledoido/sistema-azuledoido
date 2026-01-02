import redis
import time

# O host 'db' é o nome do container do banco que o Docker Compose cria
try:
    banco = redis.Redis(host='db', port=6379, decode_responses=True)
    print("--- SISTEMA AZULEDOIDO 2026 ---")
    visitas = banco.incr('contador')
    print(f"Sucesso! Este sistema já foi acessado {visitas} vezes!")
except Exception as e:
    print(f"Erro ao conectar: {e}")

# Mantém o container vivo para você conseguir ver o resultado
time.sleep(3600)

