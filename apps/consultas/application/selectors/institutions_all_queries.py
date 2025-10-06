from typing import List, Dict
from apps.consultas.infrastructure.repositories.institutions_all_repo import InstitutionsAllRepository

def instituciones_all() -> List[Dict]:
    """
    Selector para obtener todas las instituciones con su total de registros.
    """
    repo = InstitutionsAllRepository()
    return repo.obtener_instituciones_all()