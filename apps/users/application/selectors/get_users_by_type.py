from typing import Optional
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.domain.entities import Usuario

def get_users_by_type_list(tipo: int) -> Optional[list[Usuario]]:
    """
    Selector para obtener una lista de usuarios por tipo.
    """
    repo = PgUserRepository()
    return repo.get_users_by_type(tipo)