from typing import Optional
from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository

def get_record_by_id(id_registro: int) -> Optional[dict]:
    """ 
    Obtiene un registro por su ID.
    Retorna el registro o None si no existe.
    """

    repository = PostgresRegistroRepository()
    return repository.obtener_por_id(id_registro)