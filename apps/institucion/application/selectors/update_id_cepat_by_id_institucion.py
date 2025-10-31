from typing import Optional
from apps.institucion.infrastructure.repositories.institucion_repo import PgInstitucionRepository
from apps.institucion.domain.entities import Institucion
from apps.users.application.selectors.resolve_user_context import resolve_user_context
from django.core.exceptions import PermissionDenied


def update_institucion_id_cepat(id_institucion: int, id_cepat: Optional[int], user) -> Optional[Institucion]:
    """
    Comando para actualizar el id_cepat de una institución.
    Filtrado por rol:
     - Admin (35) y Cepat (37): Pueden ejecutar la actualización.
     - Otro: Se lanza PermissionDenied.
    """
    id_usuario = getattr(user, "id", None)
    context = None
    if id_usuario:
        context = resolve_user_context(int(id_usuario))

    if not context or context.get("rol_id") not in [35, 37]:
        raise PermissionDenied("No tiene permiso para modificar esta institución.")

    repo = PgInstitucionRepository()
    return repo.actualizar_id_cepat(id_institucion, id_cepat)