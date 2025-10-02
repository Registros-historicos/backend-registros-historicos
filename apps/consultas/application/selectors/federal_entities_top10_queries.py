from typing import List, Dict

from apps.consultas.infrastructure.repositories.federal_entities_repo import get_top10_entidades


def entidades_top10() -> List[Dict]:
    """
    Retorna a lo sumo 10 entidades, ordenadas desc por total.
    """
    data = get_top10_entidades()
    return sorted(data, key=lambda d: d.get("total", 0), reverse=True)[:10]