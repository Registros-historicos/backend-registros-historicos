from typing import List
from apps.institucion.infrastructure.repositories.institucion_repo import PgInstitucionRepository
from apps.institucion.domain.entities import Institucion
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def get_institutions_by_id_cepat(id_cepat: int, user) -> List[Institucion]:
    """
    Selector para listar todas las instituciones con un id_cepat coincidente.
    Filtrado por rol:
     - Admin (35) y Cepat (37): Pueden ver la lista.
     - Otro: No puede ver nada.
    """

    id_usuario = getattr(user, "id", None)
    if not id_usuario:
        return []

    context = resolve_user_context(int(id_usuario))
    if not context:
        return []

    rol_id = context["rol_id"]

    if rol_id == 35 or rol_id == 37:
        repo = PgInstitucionRepository()
        return repo.listar_con_cepat_match(id_cepat)
    else:
        return []