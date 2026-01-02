FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN pip install redis flask
# AQUI: Mudamos as permissões de arquivo no servidor do Render
RUN chmod -R 755 . 
COPY app_azuledoido.py .
COPY templates templates
CMD ["python", "app_azuledoido.py"]
