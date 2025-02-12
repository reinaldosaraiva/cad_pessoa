from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class BaseModelMixin(SQLModel, table=False):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted: bool = Field(default=False)


class Pessoa(BaseModelMixin, table=True):
    __tablename__ = "pessoas"

    nome: str = Field(max_length=100)
    email: str = Field(max_length=255)
    telefone: str = Field(max_length=20)
    data_nascimento: str = Field(max_length=10)