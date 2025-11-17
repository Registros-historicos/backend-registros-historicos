from typing import List, Dict
from apps.consultas.infrastructure.repositories.usuarios_por_estados_cepat_repo import (
    get_usuarios_por_estados_cepat_repo
)
from apps.users.application.selectors.resolve_user_context import resolve_user_context

ROL_CEPAT = 37


def usuarios_por_estados_cepat_selector(user) -> List[Dict]:
    """
    Selector que obtiene los usuarios coordinadores ubicados en los mismos estados
    que las instituciones del CEPAT autenticado.

    Args:
        user: Usuario autenticado (request.user).
    """
    # Obtener ID de usuario
    id_usuario = getattr(user, "id", None) or getattr(user, "id_usuario", None)

    if not id_usuario:
        return []

    # Resolver contexto
    context = resolve_user_context(int(id_usuario))
    if not context:
        return []

    rol_id = context.get("rol_id")

    if rol_id == ROL_CEPAT:
        return get_usuarios_por_estados_cepat_repo(id_usuario=int(id_usuario))

    return []