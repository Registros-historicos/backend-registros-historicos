from typing import Optional, List
from ...domain.entities import Cepat
from ...domain.ports import CepatRepositoryPort
from apps.users.infrastructure.repositories.pg_utils import call_fn_rows

class PgCepatRepository(CepatRepositoryPort):
    """
    Implementación (Adaptador) del repositorio de Cepat
    que utiliza funciones almacenadas de PostgreSQL.
    """

    def _map_row_to_entity(self, row: dict) -> Cepat:
        """Mapea un diccionario de fila de BD a la entidad Cepat."""
        return Cepat(**row)

    def create(self, nombre: str) -> Cepat:
        """ Llama a f_inserta_cepat """
        rows = call_fn_rows("public.f_inserta_cepat", [nombre])
        # f_inserta_cepat devuelve el registro creado
        return self._map_row_to_entity(rows[0])

    def get_all(self) -> List[Cepat]:
        """ Llama a f_busca_todos_cepat """
        rows = call_fn_rows("public.f_busca_todos_cepat", [])
        return [self._map_row_to_entity(r) for r in rows]

    def get_by_id(self, cepat_id: int) -> Optional[Cepat]:
        """ Llama a f_busca_cepat_por_id """
        rows = call_fn_rows("public.f_busca_cepat_por_id", [cepat_id])
        return self._map_row_to_entity(rows[0]) if rows else None

    def update(self, cepat_id: int, nombre: str) -> Optional[Cepat]:
        """ Llama a f_actualiza_cepat_por_id """
        rows = call_fn_rows("public.f_actualiza_cepat_por_id", [cepat_id, nombre])
        # La función devuelve el registro actualizado
        return self._map_row_to_entity(rows[0]) if rows else None

    def delete(self, cepat_id: int) -> Optional[Cepat]:
        """ Llama a f_elimina_cepat_por_id """
        rows = call_fn_rows("public.f_elimina_cepat_por_id", [cepat_id])
        # La función devuelve el registro eliminado
        return self._map_row_to_entity(rows[0]) if rows else None
