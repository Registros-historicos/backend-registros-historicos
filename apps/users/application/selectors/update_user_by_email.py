from typing import Dict, Any, Optional
from apps.users.application.services.user_comands import UserCommandsService
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.domain.entities import Usuario
from apps.users.application.selectors.resolve_user_context import resolve_user_context
from django.core.exceptions import PermissionDenied


def update_user(user, correo: str, data: Dict[str, Any]) -> Optional[Usuario]:
    """
    Comando (no Selector) para actualizar un usuario.
    Llama al servicio de comandos.
    Filtrado por rol:
     - Admin (35) y Cepat (37): Pueden actualizar.
     - Otro: Se lanza PermissionDenied.
    """

    id_usuario_autenticado = getattr(user, "id", None)
    context = None
    if id_usuario_autenticado:
        context = resolve_user_context(int(id_usuario_autenticado))

    if not context or context.get("rol_id") not in [35, 37]:
        raise PermissionDenied("No tiene permiso para actualizar usuarios.")

    repository = PgUserRepository()
    service = UserCommandsService(repository)
    new_password = data.pop('password', None)

    usuario_actualizado = service.update_user(
        correo=correo,
        data=data,
        new_password=new_password
    )
    return usuario_actualizado