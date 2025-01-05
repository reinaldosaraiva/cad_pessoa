from sqlmodel import SQLModel,Field
from datetime import datetime

class BaseModelMixin(SQLModel, table=False):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    deleted: bool = Field(default=False)
    
class Pessoa(BaseModelMixin, table=True):
    nome: str = Field(max_length=100)
    cpf: str = Field(max_length=14)
    data_nascimento: datetime = Field(default=None)