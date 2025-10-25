from dataclasses import dataclass
from typing import Optional


@dataclass
class Institucion:
    """
    Representa la entidad Institucion.
    """
    id_institucion: Optional[int]
    id_cepat: Optional[int]
    nombre: str
    clave: str
    direccion: Optional[str]
    estatus_param: Optional[int]