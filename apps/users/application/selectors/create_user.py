from typing import Optional
from apps.users.domain.entities import Usuario
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.application.selectors.resolve_user_context import resolve_user_context
from django.core.exceptions import PermissionDenied


def create_new_user(user, usuario: Usuario, pwd_hash: str) -> Optional[Usuario]:
    """
    Comando (no Selector) para crear un nuevo usuario usando el repositorio.
    Filtrado por rol:
     - Admin (35) y Cepat (37): Pueden crear usuarios.
     - Otro: Se lanza PermissionDenied.
    """
    id_usuario_autenticado = getattr(user, "id", None)
    context = None
    if id_usuario_autenticado:
        context = resolve_user_context(int(id_usuario_autenticado))

    if not context or context.get("rol_id") not in [35, 37]:
        raise PermissionDenied("No tiene permiso para crear usuarios.")
    repository = PgUserRepository()
    return repository.insertar(usuario, pwd_hash)