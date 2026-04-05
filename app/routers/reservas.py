from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Reserva, Sala, StatusReserva, StatusSala
from app.schemas.schemas import ReservaCreate, ReservaResponse
from app.security import get_current_user

router = APIRouter()


def checar_conflito(db: Session, sala_id: int, data, horario_inicio, horario_fim, excluir_id: int = None) -> bool:
    query = db.query(Reserva).filter(
        Reserva.sala_id == sala_id,
        Reserva.data == data,
        Reserva.status == StatusReserva.CONFIRMADA,
        Reserva.horario_inicio < horario_fim,
        Reserva.horario_fim > horario_inicio,
    )
    if excluir_id:
        query = query.filter(Reserva.id != excluir_id)
    return query.first() is not None


@router.post(
    "/",
    response_model=ReservaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova reserva",
    responses={
        201: {"description": "Reserva criada com sucesso"},
        401: {"description": "Não autorizado — token JWT ausente ou inválido"},
        404: {"description": "Sala não encontrada"},
        409: {"description": "Conflito de horário ou sala inativa"},
        422: {"description": "Dados inválidos"},
    },
)
def criar_reserva(
    reserva: ReservaCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    sala = db.query(Sala).filter(Sala.id == reserva.sala_id).first()
    if not sala:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala com id {reserva.sala_id} não encontrada",
        )

    if sala.status == StatusSala.INATIVA:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível reservar uma sala inativa",
        )

    if checar_conflito(db, reserva.sala_id, reserva.data, reserva.horario_inicio, reserva.horario_fim):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe reserva para esta sala no horário informado",
        )

    db_reserva = Reserva(**reserva.model_dump())
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva


@router.get(
    "/",
    response_model=List[ReservaResponse],
    summary="Listar todas as reservas",
    responses={
        200: {"description": "Lista de reservas retornada com sucesso"},
    },
)
def listar_reservas(db: Session = Depends(get_db)):
    return db.query(Reserva).all()


@router.get(
    "/{id}",
    response_model=ReservaResponse,
    summary="Buscar reserva por ID",
    responses={
        200: {"description": "Reserva encontrada"},
        404: {"description": "Reserva não encontrada"},
    },
)
def buscar_reserva(id: int, request: Request, db: Session = Depends(get_db)):
    reserva = db.query(Reserva).filter(Reserva.id == id).first()
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva com id {id} não encontrada",
        )
    return reserva


@router.patch(
    "/{id}/cancelar",
    response_model=ReservaResponse,
    summary="Cancelar reserva",
    responses={
        200: {"description": "Reserva cancelada com sucesso"},
        401: {"description": "Não autorizado — token JWT ausente ou inválido"},
        404: {"description": "Reserva não encontrada"},
        409: {"description": "Reserva já está cancelada"},
    },
)
def cancelar_reserva(
    id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    reserva = db.query(Reserva).filter(Reserva.id == id).first()
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva com id {id} não encontrada",
        )

    if reserva.status == StatusReserva.CANCELADA:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esta reserva já está cancelada",
        )

    reserva.status = StatusReserva.CANCELADA
    db.commit()
    db.refresh(reserva)
    return reserva