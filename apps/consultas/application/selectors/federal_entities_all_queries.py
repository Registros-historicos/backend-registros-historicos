from typing import List, Dict
from apps.consultas.infrastructure.repositories.federal_entities_all_repo import FederalEntitiesAllRepository

def entidades_all() -> List[Dict]:
    """
    Obtener todas las entidades federativas con su total de registros.
    """
    repo = FederalEntitiesAllRepository()
    return repo.obtener_entidades_all()