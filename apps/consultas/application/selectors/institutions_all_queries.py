from typing import List, Dict, Optional
from apps.consultas.infrastructure.repositories.institutions_all_repo import InstitutionsAllRepository
from apps.consultas.infrastructure.repositories.institutions_repo import get_instituciones_por_cepat
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def instituciones_all(user=None) -> List[Dict]:
    """
    Selector para obtener todas las instituciones con su total de registros.
    
    Args:
        user: Usuario autenticado (opcional para compatibilidad)
    
    Comportamiento:
    - Si user es None o ADMIN (rol_id=35): devuelve TODAS las instituciones
    - Si user es CEPAT (rol_id=37): devuelve solo las instituciones de su CEPAT
    
    Returns:
        Lista de instituciones con sus conteos de registros
    """
    # Si no hay usuario, retornar todas (comportamiento anterior - compatibilidad)
    if not user:
        repo = InstitutionsAllRepository()
        return repo.obtener_instituciones_all()
    
    # Obtener el ID del usuario desde el objeto request.user
    id_usuario = getattr(user, "id", None) or getattr(user, "id_usuario", None)
    
    if not id_usuario:
        # Si no se puede obtener el ID, usar comportamiento por defecto
        repo = InstitutionsAllRepository()
        return repo.obtener_instituciones_all()
    
    # Resolver contexto del usuario (rol, CEPAT, etc.)
    context = resolve_user_context(int(id_usuario))
    
    if not context:
        return []
    
    rol_id = context.get("rol_id")
    id_cepat = context.get("id_cepat")
    
    # Aplicar lógica según el rol
    if rol_id == 35:  # ADMIN - ver todas
        repo = InstitutionsAllRepository()
        return repo.obtener_instituciones_all()
    
    elif rol_id == 37:  # CEPAT - filtrar por su CEPAT
        if not id_cepat:
            return []
        # Sin límite = todas las instituciones de ese CEPAT
        return get_instituciones_por_cepat(id_cepat=id_cepat, limit=None)
    
    else:  # Otros roles - sin acceso
        return []