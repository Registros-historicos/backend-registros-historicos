from typing import Optional
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.domain.entities import Usuario
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def list_users(correo: str, user) -> Optional[Usuario]:
    """
    Selector para buscar un usuario por email.
    Permisos mejorados: Usuario puede ver sus propios datos
    """
    user_email = getattr(user, "correo", None)
    
    # PERMITIR que usuario vea sus propios datos
    if user_email and user_email == correo:
        repo = PgUserRepository()
        return repo.get_by_correo_no_login(correo)
    
    # Mantener lógica original para admins
    id_usuario_autenticado = getattr(user, "id", None)
    context = None
    if id_usuario_autenticado:
        context = resolve_user_context(int(id_usuario_autenticado))

    if context and context.get("rol_id") in [35, 37]:
        repo = PgUserRepository()
        return repo.get_by_correo_no_login(correo)
    
    return None