from datetime import datetime
from typing import Annotated
from sqlmodel import Session
from core.pessoa import models
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from database import SessionLocal
from schemas.pessoa import PessoaSchema, CreatePessoaSchema

router = APIRouter(
    prefix="/pessoa",
    tags=["pessoa"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
        

@router.get('/', status_code=status.HTTP_200_OK)
async def get_pessoas(db: db_dependency):
    
    return db.query(models.Pessoa).all()

@router.post('/add', status_code=status.HTTP_201_CREATED)
async def add_pessoa(db: db_dependency, pessoa: CreatePessoaSchema):
    
    pessoa_model = models.Pessoa(**pessoa.model_dump())
    
    db.add(pessoa_model)
    db.commit()
    return pessoa_model

@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pessoa(db: db_dependency, id: int):
    
    pessoa_model = db.query(models.Pessoa).filter(models.Pessoa.id == id).first()
    
    if not pessoa_model:
        raise HTTPException(status_code=404, detail="Person not found")
    pessoa_model.deleted = True
    
    db.commit()

@router.put('/update/{id}', status_code=status.HTTP_200_OK)
async def update_pessoa(db: db_dependency, id: int, pessoa: CreatePessoaSchema):
    
    pessoa_model = db.query(models.Pessoa).filter(models.Pessoa.id == id).first()
    
    if not pessoa_model:
        raise HTTPException(status_code=404, detail="Person not found")
    
    if pessoa_model.deleted:
        raise HTTPException(status_code=404, detail="Person not found")
    
    pessoa_model.nome = pessoa.nome
    pessoa_model.data_nascimento = pessoa.data_nascimento
    pessoa_model.cpf = pessoa.cpf
    
    pessoa_model.updated_at = datetime.now()
    
    db.add(pessoa_model)
    db.commit()
    