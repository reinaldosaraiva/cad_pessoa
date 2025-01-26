from datetime import datetime
from typing import List, Optional
from sqlmodel import Session, select
from core.pessoa.models import Pessoa
from core.pessoa.schemas import PessoaCreate, PessoaUpdate, PessoaPatch

class PessoaRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, pessoa_id: int) -> Optional[Pessoa]:
        return self.session.get(Pessoa, pessoa_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Pessoa]:
        statement = select(Pessoa).where(Pessoa.deleted == False).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def create(self, pessoa: PessoaCreate) -> Pessoa:
        db_pessoa = Pessoa(
            nome=pessoa.nome,
            cpf=pessoa.cpf,
            data_nascimento=pessoa.data_nascimento
        )
        self.session.add(db_pessoa)
        self.session.commit()
        self.session.refresh(db_pessoa)
        return db_pessoa

    def update(self, pessoa_id: int, pessoa: PessoaUpdate) -> Optional[Pessoa]:
        db_pessoa = self.get_by_id(pessoa_id)
        if not db_pessoa:
            return None
            
        pessoa_data = pessoa.model_dump(exclude_unset=True)
        for key, value in pessoa_data.items():
            setattr(db_pessoa, key, value)
        
        db_pessoa.updated_at = datetime.now()
        self.session.add(db_pessoa)
        self.session.commit()
        self.session.refresh(db_pessoa)
        return db_pessoa

    def patch(self, pessoa_id: int, pessoa: PessoaPatch) -> Optional[Pessoa]:
        db_pessoa = self.get_by_id(pessoa_id)
        if not db_pessoa:
            return None
            
        pessoa_data = pessoa.model_dump(exclude_unset=True)
        for key, value in pessoa_data.items():
            setattr(db_pessoa, key, value)
        
        db_pessoa.updated_at = datetime.now()
        self.session.add(db_pessoa)
        self.session.commit()
        self.session.refresh(db_pessoa)
        return db_pessoa

    def delete(self, pessoa_id: int) -> bool:
        db_pessoa = self.get_by_id(pessoa_id)
        if not db_pessoa:
            return False
            
        db_pessoa.deleted = True
        db_pessoa.updated_at = datetime.now()
        self.session.add(db_pessoa)
        self.session.commit()
        return True