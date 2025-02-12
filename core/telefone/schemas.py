from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, Literal
import re

class TelefoneBase(BaseModel):
    numero: str = Field(..., min_length=8, max_length=20)
    tipo: Literal["celular", "residencial", "comercial"]
    pessoa_id: int
    
    @validator('numero')
    def validate_numero(cls, v):
        # Remove caracteres não numéricos para validação
        numeros = re.sub(r'\D', '', v)
        if len(numeros) < 8 or len(numeros) > 11:
            raise ValueError('Número de telefone deve ter entre 8 e 11 dígitos')
        return v

class TelefoneCreate(TelefoneBase):
    pass

class TelefoneUpdate(BaseModel):
    numero: Optional[str] = None
    tipo: Optional[str] = None
    pessoa_id: Optional[int] = None

class TelefoneResponse(TelefoneBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted: bool

    class Config:
        from_attributes = True

class TelefoneStats(BaseModel):
    total_telefones: int
    telefones_por_tipo: dict[str, int]
    media_telefones_por_pessoa: float
    pessoas_sem_telefone: int