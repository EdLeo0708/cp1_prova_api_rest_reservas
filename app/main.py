from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import salas, reservas, auth
from app.database import Base, engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Reservas de Salas Corporativas",
    description="API REST para gerenciamento de reservas de salas de reunião",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Autenticação"])
app.include_router(salas.router, prefix="/salas", tags=["Salas"])
app.include_router(reservas.router, prefix="/reservas", tags=["Reservas"])


@app.get("/", tags=["Root"])
def root():
    return {"message": "API de Reservas de Salas Corporativas", "version": "1.0.0", "docs": "/docs"}
