from dataclasses import dataclass
from typing import Optional

@dataclass
class Parametrizacion:
    id_param: int
    nombre: str
    id_tema: int
    id_param_padre: Optional[int] = None
