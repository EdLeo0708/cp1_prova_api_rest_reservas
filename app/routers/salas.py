from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.models import Sala, StatusSala
from app.schemas.schemas import SalaCreate, SalaUpdate, SalaResponse

router = APIRouter()


@router.post(
    "/",
    response_model=SalaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar nova sala",
    responses={
        201: {"description": "Sala cadastrada com sucesso"},
        422: {"description": "Dados inválidos"},
    },
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
    responses={
        200: {"description": "Lista de salas retornada com sucesso"},
    },
)
def listar_salas(db: Session = Depends(get_db)):
    return db.query(Sala).all()


@router.get(
    "/{id}",
    response_model=SalaResponse,
    summary="Buscar sala por ID",
    responses={
        200: {"description": "Sala encontrada"},
        404: {"description": "Sala não encontrada"},
    },
)
def buscar_sala(id: int, request: Request, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter(Sala.id == id).first()
    if not sala:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala com id {id} não encontrada",
        )
    return sala


@router.patch(
    "/{id}",
    response_model=SalaResponse,
    summary="Atualizar dados da sala",
    responses={
        200: {"description": "Sala atualizada com sucesso"},
        404: {"description": "Sala não encontrada"},
    },
)
def atualizar_sala(id: int, sala_update: SalaUpdate, request: Request, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter(Sala.id == id).first()
    if not sala:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala com id {id} não encontrada",
        )
    update_data = sala_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sala, field, value)
    db.commit()
    db.refresh(sala)
    return sala


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover sala",
    responses={
        204: {"description": "Sala removida com sucesso"},
        404: {"description": "Sala não encontrada"},
    },
)
def remover_sala(id: int, request: Request, db: Session = Depends(get_db)):
    sala = db.query(Sala).filter(Sala.id == id).first()
    if not sala:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sala com id {id} não encontrada",
        )
    db.delete(sala)
    db.commit()