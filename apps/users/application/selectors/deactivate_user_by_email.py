from typing import Optional
from apps.users.infrastructure.repositories.user_repo import PgUserRepository


def deactivate_user_by_email(nombre: str) -> Optional[dict]:
    """
    Selector para crear un registro usando el repositorio.
    """

    repository = PgUserRepository()
    return repository.deactivate_by_email(nombre,0)