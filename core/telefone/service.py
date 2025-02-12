from typing import List
from sqlmodel import Session
from core.telefone.repository import TelefoneRepository
from core.telefone.schemas import TelefoneCreate, TelefoneUpdate, TelefoneResponse, TelefoneStats
from core.exceptions import ValidationError

class TelefoneService:
    def __init__(self, session: Session):
        self.repository = TelefoneRepository(session)

    async def create_telefone(self, telefone: TelefoneCreate) -> TelefoneResponse:
        # Validar limite de telefones por pessoa
        telefones_existentes = await self.repository.get_by_pessoa_id(telefone.pessoa_id)
        if len(telefones_existentes) >= 3:
            raise ValidationError("Limite máximo de 3 telefones por pessoa atingido")
        
        # Validar telefone duplicado
        for tel in telefones_existentes:
            if tel.numero == telefone.numero:
                raise ValidationError("Este número de telefone já está cadastrado para esta pessoa")
        
        return await self.repository.create(telefone)

    async def get_telefone(self, telefone_id: int) -> TelefoneResponse:
        return await self.repository.get_by_id(telefone_id)

    async def list_telefones(self) -> List[TelefoneResponse]:
        return await self.repository.get_all()

    async def list_telefones_by_pessoa(self, pessoa_id: int) -> List[TelefoneResponse]:
        return await self.repository.get_by_pessoa_id(pessoa_id)

    async def update_telefone(self, telefone_id: int, telefone: TelefoneUpdate) -> TelefoneResponse:
        # Se houver mudança de pessoa_id, validar limite na nova pessoa
        if telefone.pessoa_id:
            telefones_existentes = await self.repository.get_by_pessoa_id(telefone.pessoa_id)
            if len(telefones_existentes) >= 3:
                raise ValidationError("Limite máximo de 3 telefones por pessoa atingido")
        
        return await self.repository.update(telefone_id, telefone)

    async def delete_telefone(self, telefone_id: int) -> bool:
        return await self.repository.delete(telefone_id)

    async def get_stats(self) -> TelefoneStats:
        telefones = await self.repository.get_all()
        
        # Contagem total
        total_telefones = len(telefones)
        
        # Contagem por tipo
        telefones_por_tipo = {}
        for telefone in telefones:
            telefones_por_tipo[telefone.tipo] = telefones_por_tipo.get(telefone.tipo, 0) + 1
        
        # Buscar todas as pessoas
        query = select(Pessoa).where(Pessoa.deleted == False)
        result = await self.repository.session.execute(query)
        pessoas = result.scalars().all()
        total_pessoas = len(pessoas)
        
        # Pessoas sem telefone
        pessoas_com_telefone = set(tel.pessoa_id for tel in telefones)
        pessoas_sem_telefone = sum(1 for p in pessoas if p.id not in pessoas_com_telefone)
        
        # Média de telefones por pessoa
        media_telefones = total_telefones / total_pessoas if total_pessoas > 0 else 0
        
        return TelefoneStats(
            total_telefones=total_telefones,
            telefones_por_tipo=telefones_por_tipo,
            media_telefones_por_pessoa=round(media_telefones, 2),
            pessoas_sem_telefone=pessoas_sem_telefone
        )