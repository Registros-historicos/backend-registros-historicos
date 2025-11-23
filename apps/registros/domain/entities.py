
from dataclasses import dataclass
from typing import Optional

@dataclass
class Registro:
    id_registro: Optional[int] = None
    no_expediente: Optional[str] = None
    titulo: str = ''
    descripcion: Optional[str] = None
    fec_solicitud: Optional[str] = None
    no_titulo: Optional[str] = None
    estatus_param: Optional[int] = None
    rama_param: Optional[int] = None
    medio_ingreso_param: Optional[int] = None
    tecnologico_origen: Optional[str] = None
    anio_renovacion: Optional[int] = None
    id_subsector: Optional[int] = None
    fec_expedicion: Optional[str] = None
    archivo: Optional[str] = None
    observaciones: Optional[str] = None
    tipo_registro_param: Optional[int] = None
    tipo_ingreso_param: Optional[int] = None
    tipo_sector_param: Optional[int] = None
    id_usuario: int = 0

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
