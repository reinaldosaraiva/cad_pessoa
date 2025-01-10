from datetime import datetime
from routers.pessoa import get_db
from .utils import *

app.dependency_overrides[get_db] = override_get_db

def test_get_pessoas(test_pessoa):
    response = client.get("/pessoa/")  
    response_data = response.json()[0]
    
    assert response.status_code == 200
    assert response_data["deleted"] == False
    assert response_data["id"] == 1
    assert response_data["cpf"] == "12345678901"
    assert response_data["nome"] == "Teste"
    assert response_data["data_nascimento"] == "1980-01-01T00:00:00"
    assert "created_at" in response_data
    assert "updated_at" in response_data
    

def test_create_pessoa(test_pessoa):
    request_data = {
        "nome": "Maria",
        "cpf": "99965732587",
        "data_nascimento": "1980-01-01"
    }
    
    response = client.post("/pessoa/add", json=request_data)
    assert response.status_code == 201
  
    db = TestingSessionLocal()
    model = db.query(Pessoa).filter(Pessoa.id == 2).first()
    assert model.nome == request_data["nome"]
    assert model.cpf == request_data["cpf"]
    assert model.data_nascimento == datetime.fromisoformat(request_data["data_nascimento"])


def test_update_nome_pessoa(test_pessoa):
    request_data={
        "nome": "nome alterado neste teste",
        "cpf": "12345678901",
        "data_nascimento": "1980-01-01"
    }
    
    response = client.put('/pessoa/update/1', json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Pessoa).filter(Pessoa.id == 1).first()
    assert model.nome == "nome alterado neste teste"
    
    
def test_delete_pessoa_for_id(test_pessoa):
    response = client.delete("pessoa/delete/1")
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Pessoa).filter(Pessoa.id == 1).first()
    assert model.deleted == True




