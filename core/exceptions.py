from fastapi import HTTPException

class PessoaNotFoundError(HTTPException):
    def __init__(self, pessoa_id: int):
        super().__init__(
            status_code=404,
            detail=f"Pessoa com ID {pessoa_id} não encontrada"
        )

class TelefoneNotFoundError(HTTPException):
    def __init__(self, telefone_id: int):
        super().__init__(
            status_code=404,
            detail=f"Telefone com ID {telefone_id} não encontrado"
        )

class ValidationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=400,
            detail=detail
        )