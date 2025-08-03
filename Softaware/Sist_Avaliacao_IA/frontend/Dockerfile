# Imagem base segura e leve do Node.js
FROM node:20-slim

# Define variável para evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive

# Atualiza pacotes e remove cache para reduzir vulnerabilidades
RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y ca-certificates curl --no-install-recommends \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia apenas arquivos de dependências para melhor aproveitamento de cache
COPY package*.json ./

# Instala dependências
RUN npm install

# Copia todos os arquivos do projeto
COPY . .


RUN npm run build

# Expõe a porta padrão do Vite
EXPOSE 5173

# Comando para iniciar o frontend (modo dev, com acesso externo)
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--https", "--cert", "./cert/cert.pem", "--key", "./cert/key.pem"]
