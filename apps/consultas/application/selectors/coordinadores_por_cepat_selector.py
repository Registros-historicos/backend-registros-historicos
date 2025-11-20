from typing import List, Dict
from apps.consultas.infrastructure.repositories.coordinadores_por_cepat_repo import (
    get_coordinadores_por_usuario_cepat_repo
)
from apps.users.application.selectors.resolve_user_context import resolve_user_context

ROL_CEPAT_CONSULTA = 37

def coordinadores_por_cepat_selector(user) -> List[Dict]:
    """
    Obtiene los coordinadores asociados a las instituciones del CEPAT en sesión.
    """
    id_usuario = getattr(user, "id", None) or getattr(user, "id_usuario", None)

    if not id_usuario:
        return []

    context = resolve_user_context(int(id_usuario))
    if not context or context.get("rol_id") != ROL_CEPAT_CONSULTA:
        return []

    return get_coordinadores_por_usuario_cepat_repo(id_usuario_sesion=int(id_usuario))