import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from datetime import datetime
from main import app
from core.pessoa.models import Pessoa
from core.telefone.models import Telefone

client = TestClient(app)

@pytest.fixture
def pessoa_fixture():
    return Pessoa(
        nome="Test User",
        cpf="123.456.789-00",
        data_nascimento=datetime.now()
    )

@pytest.fixture
def telefone_fixture(pessoa_fixture, session: Session):
    session.add(pessoa_fixture)
    session.commit()
    session.refresh(pessoa_fixture)
    
    telefone = Telefone(
        numero="(11) 99999-9999",
        tipo="celular",
        pessoa_id=pessoa_fixture.id
    )
    session.add(telefone)
    session.commit()
    session.refresh(telefone)
    return telefone

def test_create_telefone(session: Session, pessoa_fixture):
    session.add(pessoa_fixture)
    session.commit()
    
    response = client.post(
        "/telefones/",
        json={
            "numero": "(11) 88888-8888",
            "tipo": "residencial",
            "pessoa_id": pessoa_fixture.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["numero"] == "(11) 88888-8888"
    assert data["tipo"] == "residencial"
    assert data["pessoa_id"] == pessoa_fixture.id

def test_get_telefone(session: Session, telefone_fixture):
    response = client.get(f"/telefones/{telefone_fixture.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["numero"] == "(11) 99999-9999"
    assert data["tipo"] == "celular"

def test_get_telefone_not_found():
    response = client.get("/telefones/999")
    assert response.status_code == 404

def test_list_telefones(session: Session, telefone_fixture):
    response = client.get("/telefones/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["numero"] == "(11) 99999-9999"

def test_list_telefones_by_pessoa(session: Session, telefone_fixture):
    response = client.get(f"/telefones/pessoa/{telefone_fixture.pessoa_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["numero"] == "(11) 99999-9999"

def test_update_telefone(session: Session, telefone_fixture):
    response = client.put(
        f"/telefones/{telefone_fixture.id}",
        json={
            "numero": "(11) 77777-7777",
            "tipo": "comercial"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["numero"] == "(11) 77777-7777"
    assert data["tipo"] == "comercial"

def test_update_telefone_not_found():
    response = client.put(
        "/telefones/999",
        json={
            "numero": "(11) 77777-7777",
            "tipo": "comercial"
        }
    )
    assert response.status_code == 404

def test_delete_telefone(session: Session, telefone_fixture):
    response = client.delete(f"/telefones/{telefone_fixture.id}")
    assert response.status_code == 200
    
    # Verificar se o telefone foi marcado como deletado
    telefone = session.get(Telefone, telefone_fixture.id)
    assert telefone.deleted == True

def test_delete_telefone_not_found():
    response = client.delete("/telefones/999")
    assert response.status_code == 404