from typing import List, Dict
from apps.consultas.infrastructure.repositories.institutions_filtered_repo import InstitutionsFilteredRepository
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def instituciones_filtradas_selector(tipo_institucion: int, user=None) -> List[Dict[str, int]]:
    """
    Selector para obtener instituciones filtradas por tipo (Federal/Descentralizado).
    Aplica filtro adicional por CEPAT si el usuario es rol CEPAT.

    Args:
        tipo_institucion: ID del parámetro de tipo de institución (122 o 123)
        user: Usuario autenticado

    Returns:
        Lista de instituciones con su conteo de registros
    """
    repo = InstitutionsFilteredRepository()
    
    # Si no hay usuario, retornar todas del tipo (comportamiento por defecto)
    if not user:
        return repo.obtener_instituciones_por_tipo(tipo_institucion)
    
    # Obtener el ID del usuario
    id_usuario = getattr(user, "id", None)
    
    if not id_usuario:
        return repo.obtener_instituciones_por_tipo(tipo_institucion)
    
    # Resolver contexto del usuario
    context = resolve_user_context(int(id_usuario))
    
    if not context:
        return []
    
    rol_id = context.get("rol_id")
    id_cepat = context.get("id_cepat")
    
    print(f"✅ Filtrado instituciones: usuario={id_usuario}, rol={rol_id}, tipo={tipo_institucion}, cepat={id_cepat}")
    
    # ADMIN (35) - Ver todas del tipo
    if rol_id == 35:
        return repo.obtener_instituciones_por_tipo(tipo_institucion)
    
    # CEPAT (37) - Filtrar por tipo Y por CEPAT
    elif rol_id == 37:
        if not id_cepat:
            print(f"⚠️ Usuario CEPAT {id_usuario} sin id_cepat asignado")
            return []
        return repo.obtener_instituciones_por_tipo_y_cepat(tipo_institucion, id_cepat)
    
    # Coordinador (36) - Filtrar por tipo Y por institución
    elif rol_id == 36:
        id_institucion = context.get("id_institucion")
        instituciones = context.get("instituciones", [])
        
        if instituciones and len(instituciones) > 0:
            # Filtrar solo las instituciones del coordinador que sean del tipo especificado
            return repo.obtener_instituciones_por_tipo_y_lista(tipo_institucion, instituciones)
        elif id_institucion:
            return repo.obtener_instituciones_por_tipo_y_lista(tipo_institucion, [id_institucion])
        else:
            return []
    
    else:
        print(f"⚠️ Rol no autorizado: {rol_id}")
        return []