#  Sistema de Autoatendimento — Panificadora/Lanchonete

Sistema de autoatendimento digital onde o cliente escaneia um QR Code na mesa, visualiza o cardápio, monta seu pedido e o envia diretamente para a cozinha/balcão — sem necessidade de atendente e sem integração com pagamento.

##  Tecnologias

- **Frontend:** React
- **Backend:** Flask (Python)
- **Banco de dados:** PostgreSQL
- **Cache/Tempo real:** Redis
- **Infraestrutura:** Docker Compose

##  Como rodar o projeto

```bash
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend: http://localhost:5001

---

##  Documento de Estratégia de Testes

### Visão Geral

Este documento descreve as principais funcionalidades do sistema, suas regras de negócio e os casos de teste definidos para garantir a qualidade da aplicação.
