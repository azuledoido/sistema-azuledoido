FROM python:3.11-slim

# Define a pasta de trabalho
WORKDIR /app

# Evita que o Python guarde logs em cache (bom para o Render)
ENV PYTHONUNBUFFERED=1

# Instala as bibliotecas necessárias
RUN pip install --no-cache-dir redis flask

# PRIMEIRO copia os arquivos, DEPOIS muda a permissão
COPY . .

# Garante que o servidor tenha permissão para ler os arquivos
RUN chmod -R 755 /app

# Comando para iniciar o seu app
CMD ["python", "app_azuledoido.py"]
