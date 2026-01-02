FROM python:3.11-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1
RUN pip install redis
COPY app_azuledoido.py .
CMD ["python", "app_azuledoido.py"]

