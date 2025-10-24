from typing import List, Dict
from apps.consultas.infrastructure.repositories.records_by_month_repo import MonthRecordsRepository


def registros_por_mes_selector(anio: int) -> List[Dict[str, int]]:
    """
    Selector para obtener conteo de registros por mes en un año específico.

    Args:
        anio: Año para filtrar los registros

    Returns:
        Lista de diccionarios con mes y total de registros
    """
    repo = MonthRecordsRepository()
    return repo.obtener_conteo_por_mes(anio)