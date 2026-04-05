# 🏢 API REST — Reservas de Salas Corporativas

> **FIAP — 3ESPR — 2026 | CP1 — Arquitetura Orientada a Serviço**  
> Professora: Damiana Costa

---

## 📌 Sobre o Projeto

API REST desenvolvida em **Python + FastAPI** para gerenciamento de reservas de salas corporativas.  
Substitui planilhas manuais por um sistema centralizado com regras de negócio, autenticação JWT e tratamento padronizado de erros.

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.11+ | Linguagem |
| FastAPI | Framework Web |
| SQLAlchemy | ORM |
| SQLite | Banco de dados (dev) |
| python-jose | JWT |
| Pydantic v2 | Validação de dados |
| Uvicorn | Servidor ASGI |
| Pytest | Testes |

---

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11 ou superior
- pip

### 1. Clone o repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd reservas_api
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute a API
```bash
uvicorn app.main:app --reload
```

A API estará disponível em: **http://localhost:8000**

### 5. Acesse a documentação interativa (Swagger)
```
http://localhost:8000/docs
```

---

## 🔐 Autenticação

A API utiliza **JWT (JSON Web Token)**.

### Credenciais disponíveis (para testes):

| Usuário | Senha |
|---|---|
| `admin` | `admin123` |
| `user` | `user123` |

### Fluxo de autenticação:
1. Faça **POST /auth/login** com `username` e `password`
2. Copie o `access_token` retornado
3. Use o token no header `Authorization: Bearer <token>`
4. Rotas protegidas: **POST /reservas/** e **PATCH /reservas/{id}/cancelar**

---

## 📡 Endpoints

### 🔑 Auth
| Método | Rota | Descrição |
|---|---|---|
| POST | `/auth/login` | Autentica e retorna JWT |

### 🏠 Salas
| Método | Rota | Descrição | Auth |
|---|---|---|---|
| POST | `/salas/` | Cadastrar sala | ❌ |
| GET | `/salas/` | Listar todas as salas | ❌ |
| GET | `/salas/{id}` | Buscar sala por ID | ❌ |
| PATCH | `/salas/{id}` | Atualizar sala | ❌ |
| DELETE | `/salas/{id}` | Remover sala | ❌ |

### 📅 Reservas
| Método | Rota | Descrição | Auth |
|---|---|---|---|
| POST | `/reservas/` | Criar reserva | ✅ |
| GET | `/reservas/` | Listar reservas | ❌ |
| GET | `/reservas/{id}` | Buscar reserva por ID | ❌ |
| PATCH | `/reservas/{id}/cancelar` | Cancelar reserva | ✅ |

---

## 📋 Regras de Negócio

- ❌ Não é permitido reservar **sala inativa**
- ❌ Não é permitido **conflito de horário** (mesmo sala, mesma data, horários sobrepostos)
- ❌ O **horário de fim** deve ser maior que o horário de início
- ✅ Reservas **canceladas não bloqueiam** horários
- 🔐 **Criação e cancelamento** de reservas exigem autenticação JWT

---

## 📄 Contrato de Resposta de Erro

Todos os erros seguem o padrão:

```json
{
  "timestamp": "2026-03-29T20:00:00+00:00",
  "status": 409,
  "error": "Conflict",
  "message": "Já existe reserva para esta sala no horário informado",
  "path": "/reservas"
}
```

### Códigos HTTP utilizados:
| Código | Descrição |
|---|---|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 422 | Unprocessable Entity |

---

## 🧪 Executar Testes

```bash
pytest tests/ -v
```

---

## 🏗️ Estrutura do Projeto

```
reservas_api/
├── app/
│   ├── main.py              # Entrypoint da aplicação
│   ├── database.py          # Configuração do banco de dados
│   ├── security.py          # JWT e autenticação
│   ├── errors.py            # Tratamento padronizado de erros
│   ├── models/
│   │   └── models.py        # Modelos SQLAlchemy (Sala, Reserva)
│   ├── schemas/
│   │   └── schemas.py       # Schemas Pydantic (validação)
│   └── routers/
│       ├── auth.py          # Rota de login
│       ├── salas.py         # CRUD de salas
│       └── reservas.py      # CRUD de reservas
├── tests/
│   └── test_api.py          # Testes automatizados
├── requirements.txt
└── README.md
```

---

## 🔒 Justificativa de Segurança

Foi escolhido **JWT (JSON Web Token)** porque:
- É **stateless**: o servidor não precisa armazenar sessões
- É **padrão da indústria** para APIs REST
- Permite **expiração** configurável do token
- Carrega **claims** (como `role`) sem consulta ao banco a cada requisição
- Suporte nativo em bibliotecas como `python-jose`

O token expira em **60 minutos** e é assinado com chave secreta via algoritmo **HS256**.

---

## 👥 Grupo

> Preencher com nomes e RMs dos integrantes.

---

## 📎 Links

- 📘 Swagger UI: `http://localhost:8000/docs`
- 📗 ReDoc: `http://localhost:8000/redoc`
