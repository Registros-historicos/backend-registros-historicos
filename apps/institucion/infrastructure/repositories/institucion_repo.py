from typing import Optional, List
from apps.institucion.domain.entities import Institucion
from apps.institucion.domain.ports import InstitucionRepositoryPort
from .pg_utils import call_fn_rows


class PgInstitucionRepository(InstitucionRepositoryPort):

    def _mapear_fila_a_entidad(self, r: dict) -> Institucion:
        """
        Mapea el diccionario de la fila a la entidad Institucion.
        Maneja inconsistencias de nombres como 'estatus_param' -> 'estatus'.
        """
        # Ejemplo de limpieza de nombres de columna (como en tu user_repo.py)
        # if 'estatus_param' in r:
        #     r['estatus'] = r.pop('estatus_param')

        return Institucion(**r)

    def actualizar_id_cepat(self, id_institucion: int, id_cepat: Optional[int]) -> Optional[Institucion]:
        """
        Llama a la función de BD para actualizar el id_cepat y devuelve la entidad completa.
        """
        rows = call_fn_rows(
            "public.f_actualiza_id_cepat_institucion",
            [id_institucion, id_cepat]
        )

        if not rows:
            return None

        # La función devuelve SETOF, pero solo esperamos una fila
        institucion_data = rows[0]
        return self._mapear_fila_a_entidad(institucion_data)

    def listar_con_cepat_match(self) -> List[Institucion]:
        """
        Devuelve una lista con todas las instituciones que coinciden en cepat.
        """
        rows = call_fn_rows("public.f_listar_instituciones_con_cepat", [])

        instituciones = []
        for r in rows:
            instituciones.append(self._mapear_fila_a_entidad(r))
        return instituciones