from typing import Optional
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.domain.entities import Usuario
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def list_users(correo: str, user) -> Optional[Usuario]:
    """
    Selector para buscar un usuario por email.
    Filtrado por rol:
     - Admin (35) y Cepat (37): Pueden buscar.
     - Otro: No puede buscar.
    """

    id_usuario_autenticado = getattr(user, "id", None)
    context = None
    if id_usuario_autenticado:
        context = resolve_user_context(int(id_usuario_autenticado))

    if not context or context.get("rol_id") not in [35, 37]:
        return None

    repo = PgUserRepository()
    return repo.get_by_correo_no_login(correo)