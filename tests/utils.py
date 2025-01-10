import pytest
from sqlalchemy import text
from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from core.pessoa.models import Pessoa

DATABASE_URL = "sqlite:///testdatabase.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@pytest.fixture
def test_pessoa():
    pessoa = Pessoa(
        nome="Teste",
        cpf="12345678901",
        data_nascimento="1990-01-01"
    )
    
    db = TestingSessionLocal()
    db.add(pessoa)
    db.commit()
    yield pessoa
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM pessoa"))
        connection.commit()
