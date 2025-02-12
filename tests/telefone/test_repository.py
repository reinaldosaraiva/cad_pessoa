import pytest
from sqlmodel import Session
from datetime import datetime
from core.telefone.repository import TelefoneRepository
from core.telefone.schemas import TelefoneCreate, TelefoneUpdate
from core.telefone.models import Telefone
from core.pessoa.models import Pessoa

@pytest.fixture
def pessoa_fixture():
    return Pessoa(
        nome="Test User",
        cpf="123.456.789-00",
        data_nascimento=datetime.now()
    )

@pytest.fixture
def telefone_fixture(pessoa_fixture):
    return Telefone(
        numero="(11) 99999-9999",
        tipo="celular",
        pessoa_id=1,
        pessoa=pessoa_fixture
    )

@pytest.mark.asyncio
async def test_create_telefone(session: Session, pessoa_fixture):
    session.add(pessoa_fixture)
    await session.commit()
    
    repository = TelefoneRepository(session)
    telefone_data = TelefoneCreate(
        numero="(11) 99999-9999",
        tipo="celular",
        pessoa_id=pessoa_fixture.id
    )
    
    telefone = await repository.create(telefone_data)
    assert telefone.numero == "(11) 99999-9999"
    assert telefone.tipo == "celular"
    assert telefone.pessoa_id == pessoa_fixture.id

@pytest.mark.asyncio
async def test_get_telefone_by_id(session: Session, telefone_fixture):
    session.add(telefone_fixture)
    await session.commit()
    
    repository = TelefoneRepository(session)
    telefone = await repository.get_by_id(telefone_fixture.id)
    
    assert telefone is not None
    assert telefone.numero == "(11) 99999-9999"

@pytest.mark.asyncio
async def test_get_all_telefones(session: Session, telefone_fixture):
    session.add(telefone_fixture)
    await session.commit()
    
    repository = TelefoneRepository(session)
    telefones = await repository.get_all()
    
    assert len(telefones) > 0
    assert telefones[0].numero == "(11) 99999-9999"

@pytest.mark.asyncio
async def test_update_telefone(session: Session, telefone_fixture):
    session.add(telefone_fixture)
    await session.commit()
    
    repository = TelefoneRepository(session)
    update_data = TelefoneUpdate(numero="(11) 88888-8888")
    
    updated_telefone = await repository.update(telefone_fixture.id, update_data)
    assert updated_telefone.numero == "(11) 88888-8888"

@pytest.mark.asyncio
async def test_delete_telefone(session: Session, telefone_fixture):
    session.add(telefone_fixture)
    await session.commit()
    
    repository = TelefoneRepository(session)
    result = await repository.delete(telefone_fixture.id)
    
    assert result is True
    deleted_telefone = await repository.get_by_id(telefone_fixture.id)
    assert deleted_telefone is None