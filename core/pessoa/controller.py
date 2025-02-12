import logging
from typing import Iterable

from fastapi import APIRouter, Body, HTTPException, Query, status

from core.pessoa.schemas import CreatePessoaIn, PessoaFilter, PessoaOut, UpdatePessoaIn
from core.pessoa.usecases import PessoaUseCaseDependency

logger = logging.getLogger(__name__)

router = APIRouter(tags=["pessoa"], prefix="/v0/api/core/pessoa")


@router.post("", summary="Create a Pessoa", status_code=status.HTTP_201_CREATED)
async def post(pessoa_usecase: PessoaUseCaseDependency, pessoa_in: CreatePessoaIn = Body(...)) -> PessoaOut:
    return await pessoa_usecase.create(create_pessoa=pessoa_in)


@router.get("", summary="List all available Pessoa", status_code=status.HTTP_200_OK)
async def list(
    pessoa_usecase: PessoaUseCaseDependency,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    filters: PessoaFilter = Query(PessoaFilter()),
) -> Iterable[PessoaOut]:
    return await pessoa_usecase.list(skip, limit, filters.model_dump(exclude_unset=True))


@router.get("/{id}", summary="Get a pessoa by ID", status_code=status.HTTP_200_OK)
async def get(id: int, pessoa_usecase: PessoaUseCaseDependency) -> PessoaOut:
    try:
        return await pessoa_usecase.get(id=id)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.put("/{id}", summary="Update a pessoa", status_code=status.HTTP_200_OK)
async def update(
    id: int, pessoa_usecase: PessoaUseCaseDependency, pessoa_update: UpdatePessoaIn = Body(...)
) -> PessoaOut:
    return await pessoa_usecase.update(id=id, update_pessoa=pessoa_update)


@router.delete("/{id}", summary="Delete a pessoa", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, pessoa_usecase: PessoaUseCaseDependency) -> None:
    await pessoa_usecase.delete(id=id)