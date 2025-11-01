from dataclasses import dataclass
from typing import Optional

@dataclass
class Investigador:
    id_investigador: Optional[int]
    nombre: str
    ape_pat: str
    ape_mat: Optional[str]
    curp: str
    sexo_param: int
    tipo_investigador_param: int


@dataclass
class Adscripcion:
    id_adscripcion: Optional[int]
    id_investigador: int
    id_institucion: int
    departamento_param: int
    programa_educativo_param: int
    cuerpo_academico_param: int
    fec_ini: str
    fec_fin: Optional[str] = None
