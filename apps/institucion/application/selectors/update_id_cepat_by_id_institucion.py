from typing import Optional
from apps.institucion.infrastructure.repositories.institucion_repo import PgInstitucionRepository
from apps.institucion.domain.entities import Institucion

def update_institucion_id_cepat(id_institucion: int, id_cepat: Optional[int]) -> Optional[Institucion]:
    """
    Comando para actualizar el id_cepat de una institución.
    """
    repo = PgInstitucionRepository()
    return repo.actualizar_id_cepat(id_institucion, id_cepat)