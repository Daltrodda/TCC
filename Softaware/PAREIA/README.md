# Microservices Project

Este projeto é uma aplicação baseada em arquitetura de microserviços com foco em escalabilidade, segurança e monitoramento.

---

## 🧱 Tecnologias Utilizadas

- **Frontend:** React + Vite + TypeScript
- **API Gateway:** FastAPI
- **Microserviços:** FastAPI (Auth, Users, ML)
- **Banco de Dados:** PostgreSQL
- **Autenticação:** JWT
- **Monitoramento:** Prometheus + Grafana
- **Machine Learning:** Scikit-learn
- **Contêinerização:** Docker + Docker Compose

---

## ▶️ Como executar em produção

### 1. Build e Deploy

```bash
cd docker/prod
docker compose -f docker-compose.prod.yml up --build -d
```

---

## 🌐 Acesso aos serviços

- **Frontend (React):** [http://localhost](http://localhost)
- **Gateway API:** [http://localhost:8000](http://localhost:8000)
- **Prometheus:** [http://localhost:9090](http://localhost:9090)
- **Grafana:** [http://localhost:3001](http://localhost:3001)
  - Login padrão: `admin` / `admin123@`

---

## 🔐 JWT Auth

- Gere token via `/token` no serviço `auth`
- Use o token como `Authorization: Bearer <token>` nas requisições ao gateway

---

## 📊 Monitoramento

Prometheus coleta métricas de todos os serviços FastAPI expostos em `/metrics`. Grafana visualiza os dados com dashboard customizado.

---

## 📦 Diretórios

```bash
frontend/       # React app
gateway/        # API Gateway com autenticação JWT
services/
  auth/         # Autenticação e geração de tokens JWT
  users/        # Serviço de usuários
  ml/           # Serviço de predição com Scikit-learn
monitoring/     # Prometheus e Grafana
docker/         # Ambientes (dev, release, prod)
```

---

## 🔐 Próximo passo: Certificados HTTPS (via Caddy ou Nginx)
(Em breve...)
