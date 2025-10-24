from typing import Optional
from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository

def get_record_by_expediente(no_expediente: str) -> Optional[dict]:
    """
    Obtiene un registro por número de expediente.
    Retorna el registro o None si no existe.
    """
    
    repository = PostgresRegistroRepository()
    return repository.obtener_por_expediente(no_expediente)