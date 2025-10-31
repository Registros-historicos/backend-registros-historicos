from typing import Optional
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.application.selectors.resolve_user_context import resolve_user_context
from django.core.exceptions import PermissionDenied

def delete_users_by_id(id_user: int, user) -> Optional[dict]:
    """
    Comando para eliminar un usuario por su ID.
    Filtrado por rol:
     - Admin (35) y Cepat (37): Pueden eliminar usuarios.
     - Otro: Se lanza PermissionDenied.
    """

    id_usuario_autenticado = getattr(user, "id", None)
    context = None
    if id_usuario_autenticado:
        context = resolve_user_context(int(id_usuario_autenticado))

    if not context or context.get("rol_id") not in [35, 37]:
        raise PermissionDenied("No tiene permiso para eliminar usuarios.")

    repository = PgUserRepository()
    return repository.delete_user_by_id(id_user)