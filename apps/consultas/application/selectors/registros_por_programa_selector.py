from typing import List, Dict
from apps.consultas.infrastructure.repositories.registros_por_programa_repo import (
    get_registros_por_programa_repo
)
from apps.users.application.selectors.resolve_user_context import resolve_user_context

ROL_COORDINADOR = 36


def registros_por_programa_selector(user) -> List[Dict]:
    """
    Lógica de negocio: Valida que el usuario sea coordinador y obtiene
    el conteo de registros por programa educativo.
    """
    id_usuario = getattr(user, "id", None) or getattr(user, "id_usuario", None)

    if not id_usuario:
        return []

    context = resolve_user_context(int(id_usuario))
    if not context:
        return []

    rol_id = context.get("rol_id")

    if rol_id == ROL_COORDINADOR:
        return get_registros_por_programa_repo(id_usuario=int(id_usuario))

    return []