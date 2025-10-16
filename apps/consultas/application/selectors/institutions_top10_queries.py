from typing import List, Dict
from apps.consultas.infrastructure.repositories.institutions_repo import get_top10_instituciones

def instituciones_top10() -> List[Dict]:
    """
    Retorna a lo sumo 10 instituciones, ordenadas desc por total.
    """
    data = get_top10_instituciones()
    return sorted(data, key=lambda d: d.get("total", 0), reverse=True)[:10]
