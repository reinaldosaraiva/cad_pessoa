from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from core.config.database import get_db
from core.pessoa.repository import PessoaRepository
from core.pessoa.schemas import (
    PessoaCreate,
    PessoaUpdate,
    PessoaPatch,
    PessoaResponse
)

router = APIRouter(prefix="/pessoas", tags=["pessoas"])

@router.get("/{pessoa_id}", response_model=PessoaResponse)
def get_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    repository = PessoaRepository(db)
    pessoa = repository.get_by_id(pessoa_id)
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return pessoa

@router.get("/", response_model=List[PessoaResponse])
def get_pessoas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1),
    db: Session = Depends(get_db)
):
    repository = PessoaRepository(db)
    return repository.get_all(skip=skip, limit=limit)

@router.post("/", response_model=PessoaResponse, status_code=201)
def create_pessoa(pessoa: PessoaCreate, db: Session = Depends(get_db)):
    repository = PessoaRepository(db)
    return repository.create(pessoa)

@router.put("/{pessoa_id}", response_model=PessoaResponse)
def update_pessoa(pessoa_id: int, pessoa: PessoaUpdate, db: Session = Depends(get_db)):
    repository = PessoaRepository(db)
    updated_pessoa = repository.update(pessoa_id, pessoa)
    if not updated_pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return updated_pessoa

@router.patch("/{pessoa_id}", response_model=PessoaResponse)
def patch_pessoa(pessoa_id: int, pessoa: PessoaPatch, db: Session = Depends(get_db)):
    repository = PessoaRepository(db)
    patched_pessoa = repository.patch(pessoa_id, pessoa)
    if not patched_pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return patched_pessoa

@router.delete("/{pessoa_id}", status_code=204)
def delete_pessoa(pessoa_id: int, db: Session = Depends(get_db)):
    repository = PessoaRepository(db)
    if not repository.delete(pessoa_id):
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
    return None