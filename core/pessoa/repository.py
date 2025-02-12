from datetime import UTC, datetime
from typing import Any, Dict, List, Optional, Type

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from core.pessoa.models import Pessoa


class PessoaRepository:
    def __init__(self, model: Type[Pessoa], database: AsyncSession) -> None:
        self.model = model
        self.database = database

    async def add(self, pessoa: Pessoa) -> Pessoa:
        self.database.add(pessoa)
        await self.database.commit()
        await self.database.refresh(pessoa)
        return pessoa

    async def get(self, id: int) -> Optional[Pessoa]:
        query = select(self.model).where(
            self.model.id == id,
            self.model.deleted == False  # noqa: E712
        )
        result = await self.database.execute(query)
        return result.scalar_one_or_none()

    async def list(
        self, skip: int = 0, limit: int = 10, filters: Dict[str, Any] = None
    ) -> List[Pessoa]:
        query = select(self.model).where(self.model.deleted == False)  # noqa: E712

        if filters:
            for field, value in filters.items():
                if value is not None:
                    query = query.where(getattr(self.model, field).ilike(f"%{value}%"))

        query = query.offset(skip).limit(limit)
        result = await self.database.execute(query)
        return result.scalars().all()

    async def update(self, pessoa: Pessoa) -> Optional[Pessoa]:
        if not pessoa.id:
            return None

        db_pessoa = await self.get(pessoa.id)
        if not db_pessoa:
            return None

        pessoa_data = pessoa.model_dump(exclude_unset=True)
        for key, value in pessoa_data.items():
            setattr(db_pessoa, key, value)

        db_pessoa.updated_at = datetime.now(UTC)
        self.database.add(db_pessoa)
        await self.database.commit()
        await self.database.refresh(db_pessoa)
        return db_pessoa

    async def delete(self, id: int, db: AsyncSession) -> bool:
        pessoa = await self.get(id)
        if not pessoa:
            return False

        pessoa.deleted = True
        pessoa.updated_at = datetime.now(UTC)
        db.add(pessoa)
        await db.commit()
        return True