from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Sala, StatusSala
from app.schemas.schemas import SalaCreate, SalaUpdate, SalaResponse
from app.errors import error_response

router = APIRouter()


@router.post(
    "/",
    response_model=SalaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar sala",
)
def cadastrar_sala(sala: SalaCreate, db: Session = Depends(get_db)):
    db_sala = Sala(**sala.model_dump())
    db.add(db_sala)
    db.commit()
    db.refresh(db_sala)
    return db_sala


@router.get(
    "/",
    response_model=List[SalaResponse],
    summary="Listar todas as salas",
)
def listar_salas(db: Session = Depends(get_db)):
    return db.query(Sala).all()


@router.get(
    "/{sala_id}",
    response_model=SalaResponse,
    summary="Buscar sala por ID",
)
def buscar_sala(sala_id: int, request: Request, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter(Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala com id {sala_id} não encontrada",
        )
    return sala


@router.patch(
    "/{sala_id}",
    response_model=SalaResponse,
    summary="Atualizar sala",
)
def atualizar_sala(sala_id: int, sala_update: SalaUpdate, request: Request, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter(Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala com id {sala_id} não encontrada",
        )
    update_data = sala_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sala, field, value)
    db.commit()
    db.refresh(sala)
    return sala


@router.delete(
    "/{sala_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover sala",
)
def remover_sala(sala_id: int, request: Request, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter(Sala.id == sala_id).first()
    if not sala:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala com id {sala_id} não encontrada",
        )
    db.delete(sala)
    db.commit()
