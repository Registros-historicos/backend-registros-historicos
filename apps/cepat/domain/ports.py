from typing import Protocol, Optional, List
from .entities import Cepat, CepatPatchResult


class CepatRepositoryPort(Protocol):
    """
    Define el contrato (interfaz) para el repositorio de Cepat.
    La lógica de negocio depende de esta interfaz, no de la implementación.
    """

    def create(self, nombre: str, id_usuario: Optional[int]) -> Cepat:
        """ Llama a f_inserta_cepat """
        ...

    def get_all(self) -> List[Cepat]:
        """ Llama a f_busca_todos_cepat """
        ...

    def get_by_id(self, cepat_id: int) -> Optional[Cepat]:
        """ Llama a f_busca_cepat_por_id """
        ...

    def update(self, cepat_id: int, nombre: str, id_usuario: Optional[int]) -> Optional[Cepat]:
        """ Llama a f_actualiza_cepat_por_id """
        ...

    def delete(self, cepat_id: int) -> Optional[Cepat]:
        """ Llama a f_elimina_cepat_por_id """
        ...

    def update_usuario(self, cepat_id: int, id_usuario: int) -> Optional[CepatPatchResult]:
        """ Llama a f_actualiza_cepat_usuario_por_id """
        ...
