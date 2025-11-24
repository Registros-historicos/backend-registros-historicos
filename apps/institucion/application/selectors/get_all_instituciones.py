from typing import List
from apps.institucion.infrastructure.repositories.institucion_repo import PgInstitucionRepository
from apps.institucion.domain.entities import Institucion
from apps.users.application.selectors.resolve_user_context import resolve_user_context

def get_all_institutions(user) -> List[Institucion]:
    """
    Selector para listar TODAS las instituciones.
    Filtrado por rol:
     - Admin (35) y Cepat (37): pueden ver la lista completa.
     - Otro: devuelve lista vacía (o podrías lanzar PermissionDenied).
    """
    id_usuario = getattr(user, "id", None)
    if not id_usuario:
        return []

    context = resolve_user_context(int(id_usuario))
    if not context:
        return []

    rol_id = context["rol_id"]

    if rol_id in (35, 37):
        repo = PgInstitucionRepository()
        return repo.listar_todas()
    else:
        # Puedes devolver [] o lanzar excepción, según tu política
        return []
