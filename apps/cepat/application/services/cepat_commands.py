from typing import Optional
from ...domain.entities import Cepat
from ...domain.ports import CepatRepositoryPort

class CepatCommandsService:
    """
        Servicio para manejar los casos de uso de escritura (Comandos).
        """
    def __init__(self, repo: CepatRepositoryPort):
        self.repo = repo

    def create_cepat(self, nombre: str, id_usuario: int) -> Cepat:
        """
        Caso de uso para crear un nuevo Cepat.
        """
        # Pasar el nuevo parámetro al repositorio
        return self.repo.create(nombre, id_usuario)

    def update_cepat(self, cepat_id: int, nombre: str, id_usuario: int) -> Optional[Cepat]:
        """
        Caso de uso para actualizar un Cepat.
        """
        # Pasar el nuevo parámetro al repositorio
        return self.repo.update(cepat_id, nombre, id_usuario)

    def delete_cepat(self, cepat_id: int) -> Optional[Cepat]:
        """
        Caso de uso para eliminar un Cepat.
        """
        return self.repo.delete(cepat_id)