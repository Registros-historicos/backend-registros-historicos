from typing import List
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.domain.entities import Usuario

def get_all_users() -> List[Usuario]:
    """
    Selector para listar todos los usuarios.
    """
    repo = PgUserRepository()
    return repo.get_all_usuers()