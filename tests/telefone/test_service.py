import pytest
from datetime import datetime
from core.telefone.service import TelefoneService
from core.telefone.schemas import TelefoneCreate
from core.pessoa.models import Pessoa
from core.exceptions import ValidationError, PessoaNotFoundError

@pytest.fixture
def pessoa_fixture():
    return Pessoa(
        nome="Test User",
        cpf="123.456.789-00",
        data_nascimento=datetime.now()
    )

@pytest.mark.asyncio
async def test_create_telefone_success(session, pessoa_fixture):
    session.add(pessoa_fixture)
    await session.commit()
    
    service = TelefoneService(session)
    telefone_data = TelefoneCreate(
        numero="(11) 99999-9999",
        tipo="celular",
        pessoa_id=pessoa_fixture.id
    )
    
    telefone = await service.create_telefone(telefone_data)
    assert telefone.numero == "(11) 99999-9999"
    assert telefone.tipo == "celular"

@pytest.mark.asyncio
async def test_create_telefone_pessoa_not_found(session):
    service = TelefoneService(session)
    telefone_data = TelefoneCreate(
        numero="(11) 99999-9999",
        tipo="celular",
        pessoa_id=999
    )
    
    with pytest.raises(PessoaNotFoundError):
        await service.create_telefone(telefone_data)

@pytest.mark.asyncio
async def test_create_telefone_limit_exceeded(session, pessoa_fixture):
    session.add(pessoa_fixture)
    await session.commit()
    
    service = TelefoneService(session)
    
    # Criar 3 telefones
    for i in range(3):
        telefone_data = TelefoneCreate(
            numero=f"(11) 9999-{i:04d}",
            tipo="celular",
            pessoa_id=pessoa_fixture.id
        )
        await service.create_telefone(telefone_data)
    
    # Tentar criar o quarto telefone
    telefone_data = TelefoneCreate(
        numero="(11) 99999-9999",
        tipo="celular",
        pessoa_id=pessoa_fixture.id
    )
    
    with pytest.raises(ValidationError) as exc_info:
        await service.create_telefone(telefone_data)
    assert "Limite máximo de 3 telefones" in str(exc_info.value.detail)

@pytest.mark.asyncio
async def test_create_duplicate_telefone(session, pessoa_fixture):
    session.add(pessoa_fixture)
    await session.commit()
    
    service = TelefoneService(session)
    telefone_data = TelefoneCreate(
        numero="(11) 99999-9999",
        tipo="celular",
        pessoa_id=pessoa_fixture.id
    )
    
    await service.create_telefone(telefone_data)
    
    # Tentar criar telefone com mesmo número
    with pytest.raises(ValidationError) as exc_info:
        await service.create_telefone(telefone_data)
    assert "já está cadastrado" in str(exc_info.value.detail)