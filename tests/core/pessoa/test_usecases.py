import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from core.pessoa.models import Pessoa
from core.pessoa.repository import PessoaRepository
from core.pessoa.schemas import CreatePessoaIn, PessoaFilter, UpdatePessoaIn
from core.pessoa.usecases import PessoaUseCase


@pytest.fixture
async def pessoa_repository(session: AsyncSession):
    return PessoaRepository(model=Pessoa, database=session)


@pytest.fixture
async def pessoa_usecase(session: AsyncSession, pessoa_repository: PessoaRepository):
    return PessoaUseCase(repository=pessoa_repository, database=session)


@pytest.fixture
async def sample_pessoa(pessoa_repository: PessoaRepository) -> Pessoa:
    pessoa = Pessoa(
        nome="João Silva",
        email="joao@example.com",
        telefone="11999999999",
        data_nascimento="1990-01-01"
    )
    return await pessoa_repository.add(pessoa)


class TestPessoaUseCase:
    async def test_create_pessoa(self, pessoa_usecase: PessoaUseCase):
        # Given
        pessoa_data = CreatePessoaIn(
            nome="Maria Santos",
            email="maria@example.com",
            telefone="11988888888",
            data_nascimento="1995-05-15"
        )

        # When
        result = await pessoa_usecase.create(pessoa_data)

        # Then
        assert result.nome == "Maria Santos"
        assert result.email == "maria@example.com"
        assert result.telefone == "11988888888"
        assert result.data_nascimento == "1995-05-15"
        assert result.id is not None

    async def test_get_pessoa(self, pessoa_usecase: PessoaUseCase, sample_pessoa: Pessoa):
        # When
        result = await pessoa_usecase.get(sample_pessoa.id)

        # Then
        assert result.id == sample_pessoa.id
        assert result.nome == sample_pessoa.nome
        assert result.email == sample_pessoa.email

    async def test_update_pessoa(self, pessoa_usecase: PessoaUseCase, sample_pessoa: Pessoa):
        # Given
        update_data = UpdatePessoaIn(
            nome="João Silva Atualizado",
            email="joao.novo@example.com",
            telefone=sample_pessoa.telefone,
            data_nascimento=sample_pessoa.data_nascimento
        )

        # When
        result = await pessoa_usecase.update(sample_pessoa.id, update_data)

        # Then
        assert result.id == sample_pessoa.id
        assert result.nome == "João Silva Atualizado"
        assert result.email == "joao.novo@example.com"
        assert result.telefone == sample_pessoa.telefone

    async def test_list_pessoas(self, pessoa_usecase: PessoaUseCase, sample_pessoa: Pessoa):
        # Given
        filters = PessoaFilter()

        # When
        results = list(await pessoa_usecase.list(skip=0, limit=10, filters=filters.model_dump(exclude_unset=True)))

        # Then
        assert len(results) >= 1
        assert any(p.id == sample_pessoa.id for p in results)

    async def test_list_pessoas_with_filter(self, pessoa_usecase: PessoaUseCase, sample_pessoa: Pessoa):
        # Given
        filters = PessoaFilter(nome=sample_pessoa.nome)

        # When
        results = list(await pessoa_usecase.list(skip=0, limit=10, filters=filters.model_dump(exclude_unset=True)))

        # Then
        assert len(results) >= 1
        assert any(p.id == sample_pessoa.id for p in results)

    async def test_delete_pessoa(self, pessoa_usecase: PessoaUseCase, sample_pessoa: Pessoa):
        # When
        await pessoa_usecase.delete(sample_pessoa.id)

        # Then
        with pytest.raises(Exception):  # Ajuste conforme sua implementação específica de exceção
            await pessoa_usecase.get(sample_pessoa.id)