from typing import List, Dict
from apps.consultas.infrastructure.repositories.records_by_status_repo import StatusRecordsRepository
from apps.users.application.selectors.resolve_user_context import resolve_user_context

def conteo_registros_por_estatus_selector(user) -> List[Dict[str, int]]:
    """
    Selector para obtener conteo de registros por estatus de solicitud según el rol del usuario.
    Roles esperados:
      - 35 → Admin (global)
      - 36 → Coordinador (por institución)
      - 37 → CEPAT (por red de instituciones asociadas)
    """
    id_usuario = getattr(user, "id", None)
    if not id_usuario:
        return []

    # Obtener contexto del usuario (rol, id_cepat, id_institucion, etc.)
    context = resolve_user_context(int(id_usuario))
    if not context:
        return []

    rol_id = context.get("rol_id")
    id_cepat = context.get("id_cepat")
    id_institucion = context.get("id_institucion")

    repo = StatusRecordsRepository()

    if rol_id == 35:
        # Admin global
        return repo.obtener_conteo_por_estatus()
    elif rol_id == 37 and id_cepat:
        # CEPAT
        return repo.obtener_conteo_por_estatus_cepat(id_cepat)
    elif rol_id == 36 and id_institucion:
        # Coordinador (institución específica)
        return repo.obtener_conteo_por_estatus_institucion(id_institucion)
    else:
        # Rol no contemplado o sin datos de contexto
        print(f"Rol no reconocido o sin contexto suficiente. id_usuario={id_usuario}, rol_id={rol_id}")
        return []
