from typing import List, Dict
from apps.consultas.infrastructure.repositories.institutions_repo import (
    get_top10_instituciones, 
    get_instituciones_por_cepat
)
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def instituciones_top10(user=None) -> List[Dict]:
    """
    Retorna top 10 instituciones según el rol del usuario:
    
    Args:
        user: Usuario autenticado (opcional para compatibilidad)
    
    Comportamiento:
    - Si user es None o ADMIN (rol_id=35): Top 10 de TODAS las instituciones
    - Si user es CEPAT (rol_id=37): Top 10 de instituciones de su CEPAT
    
    Returns:
        Lista con máximo 10 instituciones ordenadas por total de registros
    """
    # Si no hay usuario, usar el método anterior
    if not user:
        data = get_top10_instituciones()
        return sorted(data, key=lambda d: d.get("total", 0), reverse=True)[:10]
    
    # Obtener el ID del usuario
    id_usuario = getattr(user, "id", None) or getattr(user, "id_usuario", None)
    
    if not id_usuario:
        data = get_top10_instituciones()
        return sorted(data, key=lambda d: d.get("total", 0), reverse=True)[:10]
    
    # Resolver contexto del usuario
    context = resolve_user_context(int(id_usuario))
    
    if not context:
        return []
    
    rol_id = context.get("rol_id")
    id_cepat = context.get("id_cepat")
    
    # Lógica según el rol
    if rol_id == 35:  # ADMIN
        data = get_top10_instituciones()
    elif rol_id == 37:  # CEPAT
        if not id_cepat:
            return []
        data = get_instituciones_por_cepat(id_cepat=id_cepat, limit=10)
    else:
        return []
    
    return sorted(data, key=lambda d: d.get("total", 0), reverse=True)[:10]