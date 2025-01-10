from sqlmodel import SQLModel
from datetime import datetime

class CreatePessoaSchema(SQLModel):
    nome: str
    cpf: str
    data_nascimento: datetime
    
class PessoaSchema(CreatePessoaSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True