from core.telefone.models import Telefone
from core.telefone.repository import TelefoneRepository
from core.telefone.schemas import TelefoneCreate, TelefoneUpdate, TelefoneResponse

__all__ = [
    'Telefone',
    'TelefoneRepository',
    'TelefoneCreate',
    'TelefoneUpdate',
    'TelefoneResponse'
]