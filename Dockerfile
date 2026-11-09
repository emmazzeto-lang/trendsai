FROM python:3.12-slim

# Evita geracao de arquivos .pyc e buffer de logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependencias separadamente para reaproveitar cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia os fontes da aplicacao (sem copiar .env ou .tar)
COPY app/ ./app/

# Porta de comunicacao declarada
EXPOSE 8080

# Escuta em 0.0.0.0 na porta 8080 em primeiro plano
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]