# API REST — Reservas de Salas Corporativas

**FIAP — 3ESPR — 2026 | CP1 — Arquitetura Orientada a Serviço**
Professora: Damiana Costa

---

## 👤 Integrante

Edson Leonardo Pacheco Navia — RM 553737

---

## 📌 Sobre o Projeto

API REST desenvolvida em Python com FastAPI para gerenciamento de reservas de salas corporativas. O sistema substitui o controle manual por planilhas, centralizando as reservas com regras de negócio, autenticação JWT e tratamento padronizado de erros.

---

## 🚀 Como Executar

**Pré-requisitos:** Python 3.11 ou superior instalado na máquina.

**1. Clone o repositório**
```bash
git clone <URL_DO_REPOSITORIO>
cd reservas_api
```

**2. Crie e ative o ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Execute a API**
```bash
uvicorn app.main:app --reload
```

A API estará disponível em: http://localhost:8000

**5. Acesse a documentação Swagger**
```
http://localhost:8000/docs
```

---

## 🔐 Autenticação

A API utiliza JWT (JSON Web Token). Para acessar as rotas protegidas é necessário fazer login e usar o token retornado.

**Credenciais para teste:**
- Usuário: `admin` — Senha: `admin123`
- Usuário: `user` — Senha: `user123`

**Como usar:**
1. Faça POST em `/auth/login` com username e password
2. Copie o `access_token` da resposta
3. Envie o token no header: `Authorization: Bearer <token>`

Rotas que exigem autenticação: `POST /reservas/` e `PATCH /reservas/{id}/cancelar`

---

## 📡 Endpoints Disponíveis

**Autenticação**
- POST `/auth/login` — realiza login e retorna o token JWT

**Salas**
- POST `/salas/` — cadastrar nova sala
- GET `/salas/` — listar todas as salas
- GET `/salas/{id}` — buscar sala por ID
- PATCH `/salas/{id}` — atualizar dados da sala
- DELETE `/salas/{id}` — remover sala

**Reservas**
- POST `/reservas/` — criar reserva (requer autenticação)
- GET `/reservas/` — listar todas as reservas
- GET `/reservas/{id}` — buscar reserva por ID
- PATCH `/reservas/{id}/cancelar` — cancelar reserva (requer autenticação)

---

## 📋 Regras de Negócio

**Salas** possuem os campos: id, nome, capacidade, localização e status (ATIVA ou INATIVA).

**Reservas** possuem os campos: id, id da sala, nome do solicitante, e-mail, data, horário de início, horário de fim, finalidade e status (CONFIRMADA ou CANCELADA).

**Regras obrigatórias aplicadas:**
- Não é permitido criar reserva em sala com status INATIVA
- Não é permitido conflito de horário na mesma sala e data
- O horário de fim deve ser maior que o horário de início
- Reservas canceladas não bloqueiam horários para novas reservas
- Criação e cancelamento de reservas exigem autenticação JWT

---

## ⚠️ Tratamento de Erros

Todos os erros retornam um JSON padronizado no seguinte formato:

```json
{
  "timestamp": "2026-03-29T20:00:00+00:00",
  "status": 409,
  "error": "Conflict",
  "message": "Já existe reserva para esta sala no horário informado",
  "path": "/reservas"
}
```

Códigos utilizados: 200 (OK), 201 (Created), 204 (No Content), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 409 (Conflict), 422 (Unprocessable Entity).

---

## 🔒 Justificativa de Segurança

Foi escolhido JWT porque é stateless (o servidor não armazena sessões), é o padrão da indústria para APIs REST, permite expiração configurável e carrega informações do usuário sem consultar o banco a cada requisição. O token expira em 60 minutos e é assinado com algoritmo HS256.

---

## 🧪 Executar Testes

```bash
pytest tests/ -v
```

---

## 📎 Links

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json