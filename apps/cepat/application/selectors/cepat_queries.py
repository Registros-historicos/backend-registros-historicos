from typing import List, Optional
from ...domain.entities import Cepat
from ...infrastructure.repositories.pg_utils import PgCepatRepository
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def get_all_cepat(user) -> List[Cepat]:
    """
    Selector (Query) para obtener todos los Cepat.
    Filtrado por rol:
     - Admin (35) y Cepat (37).
     - Otro: No hay permisos.
    """
    repo = PgCepatRepository()

    id_usuario = getattr(user, "id", None)
    if not id_usuario:
        return []

    context = resolve_user_context(int(id_usuario))
    if not context:
        return []

    rol_id = context["rol_id"]

    # MODIFICADO: Admin y Cepat tienen los mismos permisos
    if rol_id == 35 or rol_id == 37:
        return repo.get_all()
    else:
        # 3. Otro Rol: No debe ver ningún Cepat
        return []


def get_cepat_by_id(cepat_id: int, user) -> Optional[Cepat]:
    """
    Selector (Query) para obtener un Cepat por su ID.
    Filtrado por rol:
     - Admin (35) y Cepat (37).
     - Otro: No hay permisos.
    """
    repo = PgCepatRepository()

    id_usuario = getattr(user, "id", None)
    if not id_usuario:
        return None

    context = resolve_user_context(int(id_usuario))
    if not context:
        return None

    rol_id = context["rol_id"]

    # MODIFICADO: Admin y Cepat tienen los mismos permisos
    if rol_id == 35 or rol_id == 37:
        # Pueden buscar CUALQUIER id_cepat
        return repo.get_by_id(cepat_id)
    else:
        # 3. Otro Rol: No debe ver ninguno
        return None