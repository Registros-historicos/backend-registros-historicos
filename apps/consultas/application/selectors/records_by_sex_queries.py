from typing import List, Dict
from apps.consultas.infrastructure.repositories.records_by_sex_repo import SexRecordsRepository

def registros_por_sexo_selector() -> List[Dict[str, int]]:
    """
    Selector para obtener conteo de registros por sexo de investigador.
    """
    repo = SexRecordsRepository()
    return repo.obtener_conteo_por_sexo()