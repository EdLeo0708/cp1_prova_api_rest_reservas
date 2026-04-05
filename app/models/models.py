from sqlalchemy import Column, Integer, String, Date, Time, Enum as SAEnum, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class StatusSala(str, enum.Enum):
    ATIVA = "ATIVA"
    INATIVA = "INATIVA"


class StatusReserva(str, enum.Enum):
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"


class Sala(Base):
    __tablename__ = "salas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    capacidade = Column(Integer, nullable=False)
    localizacao = Column(String(200), nullable=False)
    status = Column(SAEnum(StatusSala), default=StatusSala.ATIVA, nullable=False)

    reservas = relationship("Reserva", back_populates="sala")


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    sala_id = Column(Integer, ForeignKey("salas.id"), nullable=False)
    nome_solicitante = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    data = Column(Date, nullable=False)
    horario_inicio = Column(Time, nullable=False)
    horario_fim = Column(Time, nullable=False)
    finalidade = Column(String(300), nullable=False)
    status = Column(SAEnum(StatusReserva), default=StatusReserva.CONFIRMADA, nullable=False)

    sala = relationship("Sala", back_populates="reservas")