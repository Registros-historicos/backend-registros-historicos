from typing import List, Dict
from apps.consultas.infrastructure.repositories.departments_repo import DepartmentsRepository
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def departamentos_selector(user) -> List[Dict]:
    """
    Selector para obtener conteo de registros por departamento según rol.
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
    id_institucion = context.get("id_institucion")
    instituciones = context.get("instituciones", [])
    
    print(f"✅ Departamentos - Usuario {id_usuario}: rol={rol_id}, instituciones={instituciones if instituciones else id_institucion}")
    
    repo = DepartmentsRepository()
    
    if rol_id == 35:  # ADMIN - ve todo
        print("✅ Admin: obteniendo todos los departamentos")
        return repo.obtener_departamentos_all()
    
    elif rol_id == 36:  # COORDINADOR - puede tener múltiples instituciones
        if instituciones and len(instituciones) > 0:
            if len(instituciones) > 1:
                print(f"✅ Coordinador con múltiples instituciones: {instituciones}")
                return repo.obtener_departamentos_por_instituciones(instituciones)
            else:
                print(f"✅ Coordinador con 1 institución: {instituciones[0]}")
                return repo.obtener_departamentos_por_institucion(instituciones[0])
        elif id_institucion:
            print(f"✅ Coordinador (fallback): institución {id_institucion}")
            return repo.obtener_departamentos_por_institucion(id_institucion)
        else:
            print(f"⚠️ Usuario Coordinador {id_usuario} sin instituciones asignadas")
            return []
    
    else:
        print(f"⚠️ Rol no autorizado: id_usuario={id_usuario}, rol_id={rol_id}")
        return []