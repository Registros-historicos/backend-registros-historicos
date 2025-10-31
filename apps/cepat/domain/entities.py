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
    id_usuario: int

@dataclass
class CepatPatchResult:
    """
    Representa el resultado parcial devuelto al actualizar
    el usuario de un Cepat (f_actualiza_cepat_usuario_por_id).
    """
    id_cepat: int
    id_usuario: int