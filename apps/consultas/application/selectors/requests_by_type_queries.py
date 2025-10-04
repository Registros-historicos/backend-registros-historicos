from typing import List, Dict
from apps.consultas.infrastructure.repositories.requests_by_type_repo import get_requests_by_type

def requests_impi() -> List[Dict]:
    """
    Returns requests grouped by type (IMPI).
    """
    return get_requests_by_type("impi")

def requests_indautor() -> List[Dict]:
    """
    Returns requests grouped by type (INDAUTOR).
    """
    return get_requests_by_type("indautor")
