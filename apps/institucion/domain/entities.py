from dataclasses import dataclass
from typing import Optional


@dataclass
class Institucion:
    """
    Representa la entidad Institucion.
    Mapea la estructura de la tabla de la base de datos.
    """
    id_institucion: Optional[int]
    nombre: str
    ent_federativa_param: int
    tipo_institucion_param: int
    id_cepat: Optional[int]
    ciudad_param: int