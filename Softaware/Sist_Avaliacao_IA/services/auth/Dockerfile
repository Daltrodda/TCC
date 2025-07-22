FROM python:3.11-slim

# 1. Instalar dependências do sistema
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# 2. Criar diretório de trabalho
WORKDIR /app

# 3. Copiar e instalar dependências
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 4. Copiar o restante da aplicação
COPY ./app ./app
COPY ./cert ./cert

# 5. Comando padrão para rodar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--ssl-keyfile", "./cert/key.pem", "--ssl-certfile", "./cert/cert.pem"]
