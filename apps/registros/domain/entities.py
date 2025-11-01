
from dataclasses import dataclass
from typing import Optional

@dataclass
class Registro:
    no_expediente: str
    titulo: str
    descripcion: Optional[str]
    fec_solicitud: Optional[str]
    no_titulo: Optional[str]
    estatus_param: Optional[int]
    rama_param: Optional[int]
    medio_ingreso_param: Optional[int]
    tecnologico_origen: Optional[str]
    anio_renovacion: Optional[int]
    id_subsector: Optional[int]
    fec_expedicion: Optional[str]
    archivo: Optional[str]
    observaciones: Optional[str]
    tipo_registro_param: Optional[int]  # 44 IMPI, 45 INDAUTOR (ajusta a tus IDs)
    tipo_ingreso_param: Optional[int]   # 42 / 44 o los que uses
    id_usuario: int

@dataclass
class Investigador:
    curp: str
    nombres: str
    apellido_paterno: str
    apellido_materno: str
    sexo: str
    tipo_investigador: str
    institucion: str
    programa_educativo: str
    cuerpo_academico: str
    departamento: str
    fecha_afiliacion: Optional[str]
    fecha_fin: Optional[str]
    observaciones: Optional[str]
