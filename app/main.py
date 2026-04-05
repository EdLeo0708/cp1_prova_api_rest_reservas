from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.routers import salas, reservas, auth
from app.database import Base, engine
from datetime import datetime, timezone
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Reservas de Salas Corporativas",
    description="""
---

Bem-vindo à documentação oficial da **API de Reservas de Salas Corporativas**.

Esta API permite gerenciar salas de reunião e reservas de forma centralizada, substituindo o controle manual por planilhas.

---

## 🔐 Como se autenticar

1. Clique em **POST /auth/login** abaixo
2. Use as credenciais de teste:

| Usuário | Senha |
|---------|-------|
| `admin` | `admin123` |
| `user` | `user123` |

3. Copie o `access_token` da resposta
4. Clique no botão **Authorize** 🔒 no topo da página
5. Cole o token e clique em **Authorize**

---

## 📋 Recursos disponíveis

- **Salas** — cadastrar, listar, buscar e atualizar salas
- **Reservas** — criar, listar, buscar e cancelar reservas
- **Autenticação** — login com retorno de token JWT

---

## ⚠️ Regras de negócio

- Não é permitido reservar sala **inativa**
- Não é permitido **conflito de horário** na mesma sala
- O horário de fim deve ser **maior** que o horário de início
- Reservas **canceladas** não bloqueiam novos horários
- Criar e cancelar reservas exige **autenticação JWT**
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    mensagens = []
    for e in errors:
        campo = " -> ".join(str(loc) for loc in e["loc"] if loc != "body")
        mensagens.append(f"{campo}: {e['msg']}" if campo else e["msg"])
    return JSONResponse(
        status_code=422,
        content={
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": 422,
            "error": "Dados inválidos",
            "message": "; ".join(mensagens),
            "path": str(request.url.path),
        },
    )


app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(salas.router, prefix="/salas", tags=["Salas"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])


@app.get("/", tags=["Início"])
def root():
    return {
        "mensagem": "API de Reservas de Salas Corporativas",
        "versao": "1.0.0",
        "documentacao": "/docs"
    }