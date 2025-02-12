import pytest
from sqlmodel import SQLModel, Session, create_engine
from core.config.database import get_session
from main import app

# Usar banco de dados em memória para testes
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

# Sobrescrever a dependência de sessão do FastAPI para usar a sessão de teste
def override_get_session():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session