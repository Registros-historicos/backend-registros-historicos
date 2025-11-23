from typing import List, Dict
from apps.consultas.infrastructure.repositories.institutions_filtered_repo import InstitutionsFilteredRepository


def instituciones_filtradas_selector(tipo_institucion: int) -> List[Dict[str, int]]:
    """
    Selector para obtener instituciones filtradas por tipo (Federal/Descentralizado).

    Args:
        tipo_institucion: ID del parámetro de tipo de institución

    Returns:
        Lista de instituciones con su conteo de registros
    """
    repo = InstitutionsFilteredRepository()
    return repo.obtener_instituciones_por_tipo(tipo_institucion)