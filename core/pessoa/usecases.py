from datetime import UTC, datetime
from typing import Annotated, Any, Dict, Iterable

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config.database import get_session
from core.pessoa.models import Pessoa
from core.pessoa.repository import PessoaRepository
from core.pessoa.schemas import CreatePessoaIn, PessoaFilter, PessoaOut, UpdatePessoaIn


class PessoaUseCase:
    def __init__(self: 'PessoaUseCase', repository: PessoaRepository, database: AsyncSession) -> None:
        self.repository = repository
        self.database = database

    async def create(self: 'PessoaUseCase', create_pessoa: CreatePessoaIn) -> PessoaOut:
        """
        Cria um registro Pessoa no banco.
        """
        pessoa = Pessoa(**create_pessoa.model_dump())
        created_pessoa = await self.repository.add(pessoa)

        return PessoaOut(**created_pessoa.model_dump(exclude={'deleted'}))

    async def update(self: 'PessoaUseCase', id: int, update_pessoa: UpdatePessoaIn) -> PessoaOut:
        """
        Atualiza campos de Pessoa.
        """
        pessoa = Pessoa(
            id=id,
            updated_at=datetime.now(UTC),
            **update_pessoa.model_dump()
        )
        updated = await self.repository.update(pessoa=pessoa)

        return PessoaOut(**updated.model_dump(exclude={'deleted'}))

    async def get(self: 'PessoaUseCase', id: int) -> PessoaOut:
        """
        Obtém a Pessoa por ID.
        """
        record = await self.repository.get(id=id)
        return PessoaOut(**record.model_dump(exclude={'deleted'}))

    async def list(self: 'PessoaUseCase', skip: int, limit: int, filters: Dict[str, Any]) -> Iterable[PessoaOut]:
        """Lista Pessoas disponíveis baseado nos filtros e paginação"""
        records = await self.repository.list(skip, limit, filters)

        return (
            PessoaOut(**record.model_dump(exclude={'deleted'}))
            for record in records
        )

    async def delete(self: 'PessoaUseCase', id: int) -> None:
        """
        Soft delete (deleted=True) via repository.delete(...)
        """
        await self.repository.delete(id=id, db=self.database)


async def pessoa_usecase(
    database: AsyncSession = Depends(get_session),
) -> PessoaUseCase:
    repository = PessoaRepository(model=Pessoa, database=database)
    return PessoaUseCase(database=database, repository=repository)


PessoaUseCaseDependency = Annotated[PessoaUseCase, Depends(pessoa_usecase)]