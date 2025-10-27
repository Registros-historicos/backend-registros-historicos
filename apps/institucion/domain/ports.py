from typing import Protocol, Optional, List
from .entities import Institucion

class InstitucionRepositoryPort(Protocol):

    def actualizar_id_cepat(self, id_institucion: int, id_cepat: Optional[int]) -> Optional[Institucion]:
        """
        Llama a f_actualiza_id_cepat_institucion y devuelve la institución actualizada.
        """
        ...

    def listar_con_cepat_match(self) -> List[Institucion]:
        """
        Llama a f_listar_instituciones_con_cepat y devuelve una lista de instituciones.
        """
        ...