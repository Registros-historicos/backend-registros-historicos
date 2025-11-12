from typing import List, Dict
from apps.consultas.infrastructure.repositories.programs_educational_repo import ProgramsEducationalRepository
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def registros_por_programa_educativo_selector(user) -> List[Dict]:
    """
    Selector para obtener conteo de registros por programa educativo según rol.
    Soporta coordinadores con múltiples instituciones.
    """
    id_usuario = getattr(user, "id", None)
    
    if not id_usuario:
        print("⚠️ No se pudo obtener id_usuario")
        return []
    
    context = resolve_user_context(int(id_usuario))
    
    if not context:
        print(f"⚠️ No se pudo resolver contexto para usuario {id_usuario}")
        return []
    
    rol_id = context.get("rol_id")
    id_cepat = context.get("id_cepat")
    id_institucion = context.get("id_institucion")
    instituciones = context.get("instituciones", [])  # Lista de instituciones para coordinadores
    
    print(f"✅ Usuario {id_usuario}: rol={rol_id}, instituciones={instituciones if instituciones else id_institucion}")
    
    repo = ProgramsEducationalRepository()
    
    if rol_id == 35:  # ADMIN - ve todo
        return repo.obtener_programas_all()
    
    elif rol_id == 37:  # CEPAT - ve sus instituciones asociadas
        if not id_cepat:
            print(f"⚠️ Usuario CEPAT {id_usuario} sin id_cepat asignado")
            return []
        return repo.obtener_programas_por_cepat(id_cepat)
    
    elif rol_id == 36:  # COORDINADOR - puede tener múltiples instituciones
        # Si tiene múltiples instituciones, sumar todas
        if instituciones and len(instituciones) > 0:
            if len(instituciones) > 1:
                print(f"✅ Coordinador con múltiples instituciones, sumando datos de: {instituciones}")
                return repo.obtener_programas_por_instituciones(instituciones)
            else:
                # Solo una institución, usar el método individual
                return repo.obtener_programas_por_institucion(instituciones[0])
        elif id_institucion:
            # Fallback por si no se llenó la lista pero sí hay id_institucion
            return repo.obtener_programas_por_institucion(id_institucion)
        else:
            print(f"⚠️ Usuario Coordinador {id_usuario} sin instituciones asignadas")
            return []
    
    else:
        print(f"⚠️ Rol no reconocido: id_usuario={id_usuario}, rol_id={rol_id}")
        return []