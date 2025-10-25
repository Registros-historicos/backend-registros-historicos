from typing import List
from apps.institucion.infrastructure.repositories.institucion_repo import PgInstitucionRepository
from apps.institucion.domain.entities import Institucion

def get_institutions_by_id_cepat() -> List[Institucion]:
    """
    Selector para listar todas las instituciones con un id_cepat coincidente.
    """
    repo = PgInstitucionRepository()
    return repo.listar_con_cepat_match()