from typing import Optional, List
from ...domain.entities import Cepat, CepatPatchResult
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

    def _map_row_to_patch_result(self, row: dict) -> CepatPatchResult:
        """Mapea un diccionario de fila de BD a la entidad CepatPatchResult."""
        return CepatPatchResult(**row)

    def create(self, nombre: str, id_usuario: Optional[int]) -> Cepat:
        """ Llama a f_inserta_cepat """

        rows = call_fn_rows("public.f_inserta_cepat", [nombre, id_usuario])

        return self._map_row_to_entity(rows[0])

    def get_all(self) -> List[Cepat]:
        """ Llama a f_busca_todos_cepat """
        rows = call_fn_rows("public.f_busca_todos_cepat", [])
        return [self._map_row_to_entity(r) for r in rows]

    def get_by_id(self, cepat_id: int) -> Optional[Cepat]:
        """ Llama a f_busca_cepat_por_id """
        rows = call_fn_rows("public.f_busca_cepat_por_id", [cepat_id])
        return self._map_row_to_entity(rows[0]) if rows else None

    def update(self, cepat_id: int, nombre: str, id_usuario: Optional[int]) -> Optional[Cepat]:
        """ Llama a f_actualiza_cepat_por_id """

        rows = call_fn_rows(
            "public.f_actualiza_cepat_por_id",
            [cepat_id, nombre, id_usuario]
        )
        return self._map_row_to_entity(rows[0]) if rows else None

    def update_usuario(self, cepat_id: int, id_usuario: int) -> Optional[CepatPatchResult]:
        """ Llama a f_actualiza_cepat_usuario_por_id """
        rows = call_fn_rows(
            "public.f_actualiza_cepat_usuario_por_id",
            [cepat_id, id_usuario]
        )
        # Usa el nuevo mapper para el resultado parcial
        return self._map_row_to_patch_result(rows[0]) if rows else None

    def delete(self, cepat_id: int) -> Optional[Cepat]:
        """
        Llama a f_elimina_cepat_por_id (que retorna void).
        No procesa un retorno, solo ejecuta la llamada.
        """
        call_fn_rows("public.f_elimina_cepat_por_id", [cepat_id])
        return None

    def get_cepat_by_id_user(self, id_user: int) -> Optional[Cepat]:
        """ Llama a f_busca_cepat_por_id """
        rows = call_fn_rows("public.f_buscar_cepat_por_usuario", [id_user])
        return self._map_row_to_entity(rows[0]) if rows else None
