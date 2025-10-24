from typing import List, Optional
from ...domain.entities import Cepat
from ...infrastructure.repositories.pg_utils import PgCepatRepository


def get_all_cepat() -> List[Cepat]:
    """
    Selector (Query) para obtener todos los Cepat.
    """
    repo = PgCepatRepository()
    return repo.get_all()

def get_cepat_by_id(cepat_id: int) -> Optional[Cepat]:
    """
    Selector (Query) para obtener un Cepat por su ID.
    """
    repo = PgCepatRepository()
    return repo.get_by_id(cepat_id)
