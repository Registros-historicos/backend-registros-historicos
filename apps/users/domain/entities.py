from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Usuario:
    id_usuario: Optional[int]
    nombre: str
    ape_pat: str
    ape_mat: Optional[str]
    url_foto: Optional[str]
    correo: str
    telefono: Optional[str]
    tipo_usuario_param: int
    estatus: int
    # created_at: Optional[datetime] = None
    # updated_at: Optional[datetime] = None
