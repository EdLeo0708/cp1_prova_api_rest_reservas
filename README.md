# API REST — Reservas de Salas Corporativas

**FIAP — 3ESPR — 2026 | CP1 — Arquitetura Orientada a Serviço**
Professora: Damiana Costa

---

## 👤 Integrante

Edson Leonardo Pacheco Navia — RM 553737

---

## Sobre o Projeto

API REST desenvolvida em Python com FastAPI para gerenciamento de reservas de salas corporativas. O sistema substitui o controle manual por planilhas, centralizando as reservas com regras de negócio, autenticação JWT e tratamento padronizado de erros.

---

## Como Executar

Pré-requisitos: Python 3.11 ou superior instalado na máquina.

1. Clone o repositório e entre na pasta
2. Crie o ambiente virtual
3. Ative o ambiente virtual
4. Instale as dependências
5. Execute a API
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API estará disponível em http://localhost:8000

Acesse a documentação em http://localhost:8000/docs

---

## 🔐 Autenticação

A API utiliza JWT. Para acessar rotas protegidas faça login e use o token retornado.

Credenciais para teste:
- admin / admin123
- user / user123

Envie o token no header: Authorization: Bearer seu_token_aqui

Rotas protegidas: POST /reservas/ e PATCH /reservas/{id}/cancelar

---

## Regras de Negócio

Salas possuem os campos: id, nome, capacidade, localização e status (ATIVA ou INATIVA).

Reservas possuem os campos: id, id da sala, nome do solicitante, e-mail, data, horário de início, horário de fim, finalidade e status (CONFIRMADA ou CANCELADA).

Regras aplicadas:
- Não é permitido reservar sala com status INATIVA
- Não é permitido conflito de horário na mesma sala e data
- O horário de fim deve ser maior que o horário de início
- Reservas canceladas não bloqueiam horários para novas reservas
- Criação e cancelamento de reservas exigem autenticação JWT

---

## ⚠️ Tratamento de Erros

Todos os erros seguem este padrão:
```json
{
  "timestamp": "2026-03-29T20:00:00+00:00",
  "status": 409,
  "error": "Conflict",
  "message": "Já existe reserva para esta sala no horário informado",
  "path": "/reservas"
}
```

---

## Segurança

Foi escolhido JWT porque é stateless, padrão da indústria para APIs REST, permite expiração configurável e carrega informações do usuário sem consultar o banco a cada requisição. O token expira em 60 minutos e é assinado com algoritmo HS256.

---

## Documentação

- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc