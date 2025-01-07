from typing import Annotated
from sqlmodel import Session
from core.pessoa import models
from fastapi import APIRouter, Depends
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
    
    return db.exec(models).all()

@router.post('/add', status_code=status.HTTP_201_CREATED)
async def add_pessoa(db: db_dependency, pessoa: CreatePessoaSchema):
    
    pessoa_model = models.Pessoa(**pessoa.model_dump())
    
    db.add(pessoa_model)
    db.commit()
    return pessoa_model
    