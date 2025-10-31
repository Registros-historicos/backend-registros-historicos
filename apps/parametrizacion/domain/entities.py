from dataclasses import dataclass
from typing import Optional

@dataclass
class Parametrizacion:
    id_param: int
    nombre: str
    id_tema: int
    id_param_padre: Optional[int] = None

@dataclass
class Estado:
    id_entidad_federativa: int
    nombre_entidad: str

@dataclass
class InstitucionPorEstado:
    id_institucion: int
    nombre_institucion: str
    nombre_entidad_federativa: str
