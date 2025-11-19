from typing import List, Dict
from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository

def get_investigadores_by_registro(id_registro: int) -> List[Dict]:
    """
    Devuelve los investigadores asociados a un registro concreto.
    """
    repo = PostgresRegistroRepository()
    print(">>> repo:", repo.obtener_investigadores_por_registro)
    return repo.obtener_investigadores_por_registro(id_registro)
