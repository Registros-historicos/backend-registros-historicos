from typing import List, Dict

from apps.consultas.infrastructure.repositories.registros_por_cuerpo_academico_repo import (
    get_registros_por_cuerpo_academico_repo
)
from apps.users.application.selectors.resolve_user_context import resolve_user_context

ROL_COORDINADOR = 36


def registros_por_cuerpo_academico_selector(user) -> List[Dict]:
    """
    Lógica de negocio:
    Valida que el usuario sea coordinador y obtiene el conteo 
    de registros por cuerpo académico para la institución asignada.
    """
    id_usuario = getattr(user, "id", None) or getattr(user, "id_usuario", None)

    # Validación básica
    if not id_usuario:
        return []

    # Obtener contexto del usuario (incluye rol e institución)
    context = resolve_user_context(int(id_usuario))
    if not context:
        return []

    rol_id = context.get("rol_id")

    # Solo coordinadores pueden consultar esto
    if rol_id == ROL_COORDINADOR:
        return get_registros_por_cuerpo_academico_repo(id_usuario=int(id_usuario))

    return []
