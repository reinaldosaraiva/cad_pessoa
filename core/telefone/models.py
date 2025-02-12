from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from core.pessoa.models import BaseModelMixin, Pessoa

class Telefone(BaseModelMixin, table=True):
    numero: str = Field(max_length=20)
    tipo: str = Field(max_length=20)  # celular, residencial, comercial
    pessoa_id: Optional[int] = Field(default=None, foreign_key="pessoa.id")
    pessoa: Optional[Pessoa] = Relationship(back_populates="telefones")

# Adicionar relacionamento na classe Pessoa
Pessoa.telefones = Relationship(back_populates="pessoa", sa_relationship_kwargs={"cascade": "all, delete-orphan"})