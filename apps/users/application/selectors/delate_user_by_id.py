from typing import Optional
from apps.users.infrastructure.repositories.user_repo import PgUserRepository

def delete_users_by_id(id_user: int) -> Optional[dict]:
    """
    Selector para crear un registro usando el repositorio.
    """
    repository = PgUserRepository()
    return repository.delete_user_by_id(id_user)
