from typing import List, Dict
from apps.consultas.infrastructure.repositories.records_by_sex_repo import SexRecordsRepository
from apps.users.application.selectors.resolve_user_context import resolve_user_context

def registros_por_sexo_selector(user) -> List[Dict[str, int]]:
    """
    Selector para obtener conteo de registros por sexo de investigador según rol.
    """
    id_usuario = getattr(user, "id", None)
    
    context = resolve_user_context(int(id_usuario))
    if not context:
        return []
    
    rol_id = context["rol_id"]
    id_cepat = context.get("id_cepat")
    id_institucion = context.get("id_institucion")
    
    repo = SexRecordsRepository()
    
    if rol_id == 35:
        return repo.obtener_conteo_global_por_sexo()
    elif rol_id == 37:
        return repo.obtener_conteo_por_sexo_cepat(id_cepat)
    elif rol_id == 36:
        return repo.obtener_conteo_por_sexo_institucion(id_institucion)
    else:
        print("Usuario otro rol detectado, id_usuario:", id_usuario)
        return []