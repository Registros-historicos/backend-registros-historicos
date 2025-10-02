from typing import List, Dict
from apps.consultas.infrastructure.repositories.records_by_status_repo import StatusRecordsRepository

def conteo_registros_por_estatus_selector() -> List[Dict]:
    repo = StatusRecordsRepository()
    return repo.obtener_conteo_por_estatus()