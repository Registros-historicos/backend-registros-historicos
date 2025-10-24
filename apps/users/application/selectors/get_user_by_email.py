from typing import Optional
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.domain.entities import Usuario

def list_users(correo: str) -> Optional[Usuario]:
    """
    Selector para buscar un usuario por email.
    """
    repo = PgUserRepository()
    return repo.get_by_correo_no_login(correo)