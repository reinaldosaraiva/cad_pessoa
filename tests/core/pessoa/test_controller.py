import pytest
from fastapi import status
from httpx import AsyncClient

from core.pessoa.models import Pessoa
from core.pessoa.repository import PessoaRepository


@pytest.fixture
async def sample_pessoa(session) -> Pessoa:
    repository = PessoaRepository(model=Pessoa, database=session)
    pessoa = Pessoa(
        nome="João Silva",
        email="joao@example.com",
        telefone="11999999999",
        data_nascimento="1990-01-01"
    )
    return await repository.add(pessoa)


class TestPessoaController:
    async def test_create_pessoa(self, client: AsyncClient):
        # Given
        pessoa_data = {
            "nome": "Maria Santos",
            "email": "maria@example.com",
            "telefone": "11988888888",
            "data_nascimento": "1995-05-15"
        }

        # When
        response = await client.post("/v0/api/core/pessoa", json=pessoa_data)

        # Then
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["nome"] == pessoa_data["nome"]
        assert data["email"] == pessoa_data["email"]
        assert "id" in data

    async def test_get_pessoa(self, client: AsyncClient, sample_pessoa: Pessoa):
        # When
        response = await client.get(f"/v0/api/core/pessoa/{sample_pessoa.id}")

        # Then
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == sample_pessoa.id
        assert data["nome"] == sample_pessoa.nome
        assert data["email"] == sample_pessoa.email

    async def test_get_pessoa_not_found(self, client: AsyncClient):
        # When
        response = await client.get("/v0/api/core/pessoa/999999")

        # Then
        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_update_pessoa(self, client: AsyncClient, sample_pessoa: Pessoa):
        # Given
        update_data = {
            "nome": "João Silva Atualizado",
            "email": "joao.novo@example.com",
            "telefone": sample_pessoa.telefone,
            "data_nascimento": sample_pessoa.data_nascimento
        }

        # When
        response = await client.put(
            f"/v0/api/core/pessoa/{sample_pessoa.id}",
            json=update_data
        )

        # Then
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["nome"] == update_data["nome"]
        assert data["email"] == update_data["email"]
        assert data["telefone"] == sample_pessoa.telefone

    async def test_list_pessoas(self, client: AsyncClient, sample_pessoa: Pessoa):
        # When
        response = await client.get("/v0/api/core/pessoa")

        # Then
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(p["id"] == sample_pessoa.id for p in data)

    async def test_list_pessoas_with_filter(self, client: AsyncClient, sample_pessoa: Pessoa):
        # When
        response = await client.get("/v0/api/core/pessoa", params={"nome": sample_pessoa.nome})

        # Then
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(p["id"] == sample_pessoa.id for p in data)

    async def test_delete_pessoa(self, client: AsyncClient, sample_pessoa: Pessoa):
        # When
        response = await client.delete(f"/v0/api/core/pessoa/{sample_pessoa.id}")

        # Then
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deletion
        get_response = await client.get(f"/v0/api/core/pessoa/{sample_pessoa.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND