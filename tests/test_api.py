import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

# ─── Test Database Setup ──────────────────────────────────────────────────────
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_reservas.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)
client = TestClient(app)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_token():
    r = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    return r.json()["access_token"]


def auth_headers():
    return {"Authorization": f"Bearer {get_token()}"}


def criar_sala_ativa():
    r = client.post("/salas/", json={
        "nome": "Sala A",
        "capacidade": 10,
        "localizacao": "2º andar",
        "status": "ATIVA",
    })
    return r.json()["id"]


# ─── Auth Tests ───────────────────────────────────────────────────────────────

def test_login_sucesso():
    r = client.post("/auth/login", json={"username": "admin", "password": "admin123"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_invalido():
    r = client.post("/auth/login", json={"username": "admin", "password": "errado"})
    assert r.status_code == 401


# ─── Sala Tests ───────────────────────────────────────────────────────────────

def test_cadastrar_sala():
    r = client.post("/salas/", json={"nome": "Sala B", "capacidade": 5, "localizacao": "1º andar"})
    assert r.status_code == 201
    assert r.json()["status"] == "ATIVA"


def test_listar_salas():
    r = client.get("/salas/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_buscar_sala_nao_existente():
    r = client.get("/salas/99999")
    assert r.status_code == 404


# ─── Reserva Tests ────────────────────────────────────────────────────────────

def test_criar_reserva_sem_autenticacao():
    sala_id = criar_sala_ativa()
    r = client.post("/reservas/", json={
        "sala_id": sala_id,
        "nome_solicitante": "João",
        "email": "joao@empresa.com",
        "data": "2026-06-01",
        "horario_inicio": "09:00:00",
        "horario_fim": "10:00:00",
        "finalidade": "Reunião",
    })
    assert r.status_code == 403


def test_criar_reserva_com_autenticacao():
    sala_id = criar_sala_ativa()
    r = client.post("/reservas/", json={
        "sala_id": sala_id,
        "nome_solicitante": "Maria",
        "email": "maria@empresa.com",
        "data": "2026-06-10",
        "horario_inicio": "14:00:00",
        "horario_fim": "15:00:00",
        "finalidade": "Apresentação",
    }, headers=auth_headers())
    assert r.status_code == 201
    assert r.json()["status"] == "CONFIRMADA"


def test_conflito_de_horario():
    sala_id = criar_sala_ativa()
    headers = auth_headers()
    payload = {
        "sala_id": sala_id,
        "nome_solicitante": "Pedro",
        "email": "pedro@empresa.com",
        "data": "2026-07-01",
        "horario_inicio": "10:00:00",
        "horario_fim": "11:00:00",
        "finalidade": "Reunião A",
    }
    client.post("/reservas/", json=payload, headers=headers)
    # Segunda reserva no mesmo horário deve falhar
    payload["nome_solicitante"] = "Ana"
    payload["email"] = "ana@empresa.com"
    r = client.post("/reservas/", json=payload, headers=headers)
    assert r.status_code == 409


def test_reserva_sala_inativa():
    r = client.post("/salas/", json={"nome": "Sala Inativa", "capacidade": 5, "localizacao": "3º andar", "status": "INATIVA"})
    sala_id = r.json()["id"]
    resp = client.post("/reservas/", json={
        "sala_id": sala_id,
        "nome_solicitante": "Carlos",
        "email": "carlos@empresa.com",
        "data": "2026-08-01",
        "horario_inicio": "10:00:00",
        "horario_fim": "11:00:00",
        "finalidade": "Teste",
    }, headers=auth_headers())
    assert resp.status_code == 409


def test_cancelar_reserva():
    sala_id = criar_sala_ativa()
    headers = auth_headers()
    r = client.post("/reservas/", json={
        "sala_id": sala_id,
        "nome_solicitante": "Lúcia",
        "email": "lucia@empresa.com",
        "data": "2026-09-01",
        "horario_inicio": "08:00:00",
        "horario_fim": "09:00:00",
        "finalidade": "Daily",
    }, headers=headers)
    reserva_id = r.json()["id"]
    r2 = client.patch(f"/reservas/{reserva_id}/cancelar", headers=headers)
    assert r2.status_code == 200
    assert r2.json()["status"] == "CANCELADA"


def test_cancelar_sem_autenticacao():
    sala_id = criar_sala_ativa()
    headers = auth_headers()
    r = client.post("/reservas/", json={
        "sala_id": sala_id,
        "nome_solicitante": "Teste",
        "email": "teste@empresa.com",
        "data": "2026-10-01",
        "horario_inicio": "11:00:00",
        "horario_fim": "12:00:00",
        "finalidade": "Teste",
    }, headers=headers)
    reserva_id = r.json()["id"]
    r2 = client.patch(f"/reservas/{reserva_id}/cancelar")
    assert r2.status_code == 403


def test_horario_fim_menor_que_inicio():
    sala_id = criar_sala_ativa()
    r = client.post("/reservas/", json={
        "sala_id": sala_id,
        "nome_solicitante": "Erro",
        "email": "erro@empresa.com",
        "data": "2026-11-01",
        "horario_inicio": "15:00:00",
        "horario_fim": "14:00:00",
        "finalidade": "Teste inválido",
    }, headers=auth_headers())
    assert r.status_code == 422
