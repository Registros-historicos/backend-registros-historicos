from typing import Optional
from ...domain.entities import Cepat
from ...domain.ports import CepatRepositoryPort

class CepatCommandsService:
    """
    Servicio para manejar los casos de uso de escritura (Comandos).
    """
    def __init__(self, repo: CepatRepositoryPort):
        self.repo = repo

    def create_cepat(self, nombre: str) -> Cepat:
        """
        Caso de uso para crear un nuevo Cepat.
        """
        return self.repo.create(nombre)

    def update_cepat(self, cepat_id: int, nombre: str) -> Optional[Cepat]:
        """
        Caso de uso para actualizar un Cepat.
        """
        return self.repo.update(cepat_id, nombre)

    def delete_cepat(self, cepat_id: int) -> Optional[Cepat]:
        """
        Caso de uso para eliminar un Cepat.
        """
        return self.repo.delete(cepat_id)