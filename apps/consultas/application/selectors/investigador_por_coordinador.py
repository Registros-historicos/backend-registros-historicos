from typing import List, Dict
from apps.consultas.infrastructure.repositories.investigadores_por_coordinador_repo import (
    get_investigadores_por_coordinador_repo
)
from apps.users.application.selectors.resolve_user_context import resolve_user_context

# ID de rol para Coordinador (basado en tu ViewSet de ejemplo)
ROL_COORDINADOR = 36


def investigadores_por_coordinador_selector(user) -> List[Dict]:
    """
    Retorna la lista de investigadores asociados a la institución
    del usuario coordinador autenticado.

    Args:
        user: Objeto de usuario autenticado de Django (request.user)

    Comportamiento:
    - Si el usuario NO es Coordinador (rol_id=36), retorna una lista vacía.
    - Si ES Coordinador, llama al repositorio para buscar a sus investigadores.
    """

    # Obtener el ID del usuario de forma segura
    id_usuario = getattr(user, "id", None) or getattr(user, "id_usuario", None)

    if not id_usuario:
        return []

    # Resolver contexto del usuario para obtener su ROL
    context = resolve_user_context(int(id_usuario))

    if not context:
        return []

    rol_id = context.get("rol_id")

    # Lógica de negocio: Solo los coordinadores pueden ver sus investigadores
    if rol_id == ROL_COORDINADOR:
        # Llamar al repositorio con el ID del coordinador
        return get_investigadores_por_coordinador_repo(id_usuario=int(id_usuario))
    else:
        # Cualquier otro rol (Admin, CEPAT, etc.) no verá nada en este endpoint
        return []