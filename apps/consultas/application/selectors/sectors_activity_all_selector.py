from typing import List, Dict
from apps.consultas.infrastructure.repositories.sectors_activity_repo import get_sectores_por_actividad


def sectores_actividad_all() -> List[Dict]:
    """
    Retorna TODOS los sectores, ordenados desc por total.
    Sin límite de registros.
    """
    data = get_sectores_por_actividad()
    return sorted(data, key=lambda d: d.get("total", 0), reverse=True)