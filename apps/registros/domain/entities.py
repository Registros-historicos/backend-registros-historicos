from dataclasses import dataclass

@dataclass
class Registro:
    id_registro: int = None
    no_expediente: str = None
    titulo: str = None
    tipo_ingreso_param: str = None
    id_usuario: int = None
    rama_param: str = None
    fec_expedicion: str = None
    observaciones: str = None
    archivo: str = None
    estatus_param: str = None
    medio_ingreso_param: str = None
    tipo_registro_param: str = None
    fec_solicitud: str = None
    descripcion: str = None
    tipo_sector_param: str = None
    id_nstituciones : list[int] = None
    instituciones : list[str] = None