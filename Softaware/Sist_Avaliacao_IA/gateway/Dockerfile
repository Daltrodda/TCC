FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para dentro da imagem
COPY ./app ./app
COPY ./certs ./certs

# Expõe a porta do serviço
EXPOSE 8000

# Comando padrão para subir a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--ssl-keyfile", "certs/key.pem", "--ssl-certfile", "certs/cert.pem"]

