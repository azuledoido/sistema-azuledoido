FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
# AQUI: Instalamos as duas bibliotecas necessárias agora
RUN pip install redis flask
COPY app_azuledoido.py .
CMD ["python", "app_azuledoido.py"]
