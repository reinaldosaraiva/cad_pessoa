from sqlmodel import select, Session
from datetime import datetime
from typing import List, Optional
from core.telefone.models import Telefone
from core.pessoa.models import Pessoa
from core.telefone.schemas import TelefoneCreate, TelefoneUpdate
from core.exceptions import PessoaNotFoundError, TelefoneNotFoundError

class TelefoneRepository:
    def __init__(self, session: Session):
        self.session = session

    async def _validate_pessoa(self, pessoa_id: int) -> None:
        query = select(Pessoa).where(Pessoa.id == pessoa_id, Pessoa.deleted == False)
        result = await self.session.execute(query)
        pessoa = result.scalar_one_or_none()
        if not pessoa:
            raise PessoaNotFoundError(pessoa_id)

    async def create(self, telefone: TelefoneCreate) -> Telefone:
        # Validar se a pessoa existe
        await self._validate_pessoa(telefone.pessoa_id)
        
        db_telefone = Telefone(**telefone.model_dump())
        self.session.add(db_telefone)
        await self.session.commit()
        await self.session.refresh(db_telefone)
        return db_telefone

    async def get_by_id(self, telefone_id: int) -> Optional[Telefone]:
        query = select(Telefone).where(Telefone.id == telefone_id, Telefone.deleted == False)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self) -> List[Telefone]:
        query = select(Telefone).where(Telefone.deleted == False)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_pessoa_id(self, pessoa_id: int) -> List[Telefone]:
        query = select(Telefone).where(Telefone.pessoa_id == pessoa_id, Telefone.deleted == False)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self, telefone_id: int, telefone_data: TelefoneUpdate) -> Optional[Telefone]:
        db_telefone = await self.get_by_id(telefone_id)
        if not db_telefone:
            return None
        
        telefone_data_dict = telefone_data.model_dump(exclude_unset=True)
        for key, value in telefone_data_dict.items():
            setattr(db_telefone, key, value)
        
        db_telefone.updated_at = datetime.now()
        await self.session.commit()
        await self.session.refresh(db_telefone)
        return db_telefone

    async def delete(self, telefone_id: int) -> bool:
        db_telefone = await self.get_by_id(telefone_id)
        if not db_telefone:
            return False
        
        db_telefone.deleted = True
        db_telefone.updated_at = datetime.now()
        await self.session.commit()
        return True