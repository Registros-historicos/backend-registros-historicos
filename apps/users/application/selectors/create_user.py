from typing import Optional

from apps.users.domain.entities import Usuario
from apps.users.infrastructure.repositories.user_repo import PgUserRepository


def create_new_user(usuario: Usuario, pwd_hash: str) -> Optional[Usuario]:
    """
    Selector para crear un registro usando el repositorio.
    """
    repository = PgUserRepository()

    # 4. (La corrección principal) Llamamos a .insertar() en lugar de .create()
    return repository.insertar(usuario, pwd_hash)