from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List
from core.config.database import get_session
from core.telefone.service import TelefoneService
from core.telefone.schemas import TelefoneCreate, TelefoneUpdate, TelefoneResponse, TelefoneStats
from core.exceptions import TelefoneNotFoundError, ValidationError

router = APIRouter(prefix="/telefones", tags=["telefones"])

@router.post("/", response_model=TelefoneResponse, 
             summary="Criar novo telefone",
             description="Cria um novo registro de telefone associado a uma pessoa")
async def create_telefone(
    telefone: TelefoneCreate,
    session: Session = Depends(get_session)
) -> TelefoneResponse:
    """
    Cria um novo telefone com os seguintes parâmetros:
    
    - **numero**: Número do telefone no formato (XX) XXXXX-XXXX
    - **tipo**: Tipo do telefone (celular, residencial ou comercial)
    - **pessoa_id**: ID da pessoa associada ao telefone
    """
    service = TelefoneService(session)
    return await service.create_telefone(telefone)

@router.get("/{telefone_id}", response_model=TelefoneResponse,
             summary="Obter telefone por ID",
             description="Retorna os detalhes de um telefone específico")
async def get_telefone(
    telefone_id: int,
    session: Session = Depends(get_session)
) -> TelefoneResponse:
    """
    Busca um telefone pelo seu ID:
    
    - **telefone_id**: ID único do telefone
    """
    repository = TelefoneRepository(session)
    telefone = await repository.get_by_id(telefone_id)
    if not telefone:
        raise HTTPException(status_code=404, detail="Telefone não encontrado")
    return telefone

@router.get("/", response_model=List[TelefoneResponse])
async def list_telefones(
    session: Session = Depends(get_session)
):
    repository = TelefoneRepository(session)
    return await repository.get_all()

@router.get("/pessoa/{pessoa_id}", response_model=List[TelefoneResponse])
async def list_telefones_by_pessoa(
    pessoa_id: int,
    session: Session = Depends(get_session)
):
    repository = TelefoneRepository(session)
    return await repository.get_by_pessoa_id(pessoa_id)

@router.put("/{telefone_id}", response_model=TelefoneResponse)
async def update_telefone(
    telefone_id: int,
    telefone: TelefoneUpdate,
    session: Session = Depends(get_session)
):
    repository = TelefoneRepository(session)
    updated_telefone = await repository.update(telefone_id, telefone)
    if not updated_telefone:
        raise HTTPException(status_code=404, detail="Telefone não encontrado")
    return updated_telefone

@router.delete("/{telefone_id}")
async def delete_telefone(
    telefone_id: int,
    session: Session = Depends(get_session)
):
    service = TelefoneService(session)
    if not await service.delete_telefone(telefone_id):
        raise TelefoneNotFoundError(telefone_id)
    return {"message": "Telefone deletado com sucesso"}

@router.get("/stats/overview", response_model=TelefoneStats,
            summary="Obter estatísticas dos telefones",
            description="Retorna estatísticas gerais sobre os telefones cadastrados")
async def get_telefone_stats(
    session: Session = Depends(get_session)
) -> TelefoneStats:
    """
    Retorna estatísticas sobre os telefones cadastrados:
    
    - Total de telefones
    - Quantidade de telefones por tipo
    - Média de telefones por pessoa
    - Quantidade de pessoas sem telefone
    """
    service = TelefoneService(session)
    return await service.get_stats()