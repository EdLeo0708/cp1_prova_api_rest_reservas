from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date, time
from app.models.models import StatusSala, StatusReserva


# ─── Sala Schemas ─────────────────────────────────────────────────────────────

class SalaBase(BaseModel):
    nome: str
    capacidade: int
    localizacao: str


class SalaCreate(SalaBase):
    status: Optional[StatusSala] = StatusSala.ATIVA

    @field_validator("capacidade")
    @classmethod
    def capacidade_positiva(cls, v):
        if v <= 0:
            raise ValueError("Capacidade deve ser maior que zero")
        return v


class SalaUpdate(BaseModel):
    nome: Optional[str] = None
    capacidade: Optional[int] = None
    localizacao: Optional[str] = None
    status: Optional[StatusSala] = None


class SalaResponse(SalaBase):
    id: int
    status: StatusSala

    model_config = {"from_attributes": True}


# ─── Reserva Schemas ──────────────────────────────────────────────────────────

class ReservaBase(BaseModel):
    sala_id: int
    nome_solicitante: str
    email: EmailStr
    data: date
    horario_inicio: time
    horario_fim: time
    finalidade: str


class ReservaCreate(ReservaBase):
    @field_validator("horario_fim")
    @classmethod
    def fim_maior_que_inicio(cls, v, info):
        inicio = info.data.get("horario_inicio")
        if inicio and v <= inicio:
            raise ValueError("Horário de fim deve ser maior que o horário de início")
        return v


class ReservaResponse(ReservaBase):
    id: int
    status: StatusReserva

    model_config = {"from_attributes": True}


# ─── Auth Schemas ─────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ─── Error Schema ─────────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    timestamp: str
    status: int
    error: str
    message: str
    path: str
