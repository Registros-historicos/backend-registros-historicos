from typing import List, Dict
from apps.consultas.infrastructure.repositories.sectors_activity_repo import get_sectores_por_actividad

def sectores_actividad_all(user=None) -> List[Dict]:
    """
    Retorna TODOS los sectores, ordenados desc por total.
    Sin límite de registros.
    Selector final - delega al repositorio con lógica de usuario
    """
    return get_sectores_por_actividad(user)