from typing import List
from .entities import Parametrizacion

class ParametrizacionRepositoryPort:
    """Interfaz del repositorio (puerto)"""
    def get_all(self) -> List[Parametrizacion]:
        raise NotImplementedError

    def get_by_tema(self, id_tema: int) -> List[Parametrizacion]:
        raise NotImplementedError
