from typing import List
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.domain.entities import Usuario
from apps.users.application.selectors.resolve_user_context import resolve_user_context

def get_all_users(user) -> List[Usuario]:
    """
    Selector para listar todos los usuarios.
    Filtrado por rol:
     - Admin (35) y Cepat (37): Pueden ver la lista.
     - Otro: No puede ver nada.
    """

    id_usuario_autenticado = getattr(user, "id", None)
    if not id_usuario_autenticado:
        return []

    context = resolve_user_context(int(id_usuario_autenticado))
    if not context:
        return []

    rol_id = context["rol_id"]

    if rol_id == 35 or rol_id == 37:
        repo = PgUserRepository()
        return repo.get_all_usuers()
    else:
        return []