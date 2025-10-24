from typing import List, Dict
from apps.consultas.infrastructure.repositories.economic_sectors_repo import EconomicSectorsRepository

def conteo_registros_por_sector_selector() -> List[Dict]:
    """
    Selector que obtiene el conteo de registros agrupados por sector económico.
    """
    repository = EconomicSectorsRepository()
    return repository.obtener_conteo_por_sector()