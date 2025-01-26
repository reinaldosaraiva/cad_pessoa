from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class PessoaBase(BaseModel):
    nome: str = Field(..., max_length=100)
    cpf: str = Field(..., max_length=14)
    data_nascimento: datetime

class PessoaCreate(PessoaBase):
    pass

class PessoaUpdate(PessoaBase):
    nome: Optional[str] = Field(None, max_length=100)
    cpf: Optional[str] = Field(None, max_length=14)
    data_nascimento: Optional[datetime] = None

class PessoaPatch(BaseModel):
    nome: Optional[str] = Field(None, max_length=100)
    cpf: Optional[str] = Field(None, max_length=14)
    data_nascimento: Optional[datetime] = None

class PessoaResponse(PessoaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool

    class Config:
        from_attributes = True