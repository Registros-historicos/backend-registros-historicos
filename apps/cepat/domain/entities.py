from dataclasses import dataclass
from typing import Optional

@dataclass
class Cepat:
    """
    Representa la entidad de negocio 'Cepat'.
    Coincide con la estructura devuelta por las funciones de PostgreSQL.
    """
    id_cepat: int
    nombre: str
