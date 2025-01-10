from datetime import datetime
import pytest
from sqlalchemy import text
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from core.pessoa.models import Pessoa
from main import app
from fastapi.testclient import TestClient

DATABASE_URL = "sqlite:///testdatabase.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

SQLModel.metadata.create_all(engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        

client = TestClient(app)
        

@pytest.fixture
def test_pessoa():
    pessoa = Pessoa(
        nome="Teste",
        cpf="12345678901",
        data_nascimento=datetime.strptime("1980-01-01", "%Y-%m-%d").date()
    )
    
    db = TestingSessionLocal()
    db.add(pessoa)
    db.commit()
    
    yield pessoa
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM pessoa"))
        connection.commit()
