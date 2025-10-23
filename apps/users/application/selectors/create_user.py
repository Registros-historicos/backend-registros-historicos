from typing import Optional

from apps.users.domain.entities import Usuario
from apps.users.infrastructure.repositories.user_repo import PgUserRepository


def create_new_user(nombre: Usuario,pwd_hash: str) -> int:
    """
    Selector para crear un registro usando el repositorio.
    """

    repository = PgUserRepository()
    return repository.create(nombre, pwd_hash)