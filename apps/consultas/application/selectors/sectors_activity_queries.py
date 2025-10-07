from typing import List, Dict
from apps.consultas.infrastructure.repositories.sectors_activity_repo import get_sectores_por_actividad


def sectores_actividad_top10() -> List[Dict]:
    """
    Retorna a lo sumo 10 sectores, ordenados desc por total.
    """
    data = get_sectores_por_actividad()
    return sorted(data, key=lambda d: d.get("total", 0), reverse=True)[:10]