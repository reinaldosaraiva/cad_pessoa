from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class PessoaBase(BaseModel):
    nome: str = Field(..., max_length=100)
    email: EmailStr
    telefone: str = Field(..., max_length=20)
    data_nascimento: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')


class CreatePessoaIn(PessoaBase):
    pass


class UpdatePessoaIn(BaseModel):
    nome: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=20)
    data_nascimento: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}-\d{2}$')


class PessoaFilter(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None


class PessoaOut(PessoaBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True