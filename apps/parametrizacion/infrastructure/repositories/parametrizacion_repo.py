from django.db import connection
from apps.parametrizacion.domain.entities import Parametrizacion, Estado, InstitucionPorEstado
from apps.parametrizacion.domain.ports import ParametrizacionRepositoryPort

class ParametrizacionRepository(ParametrizacionRepositoryPort):

    def get_all(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_param, nombre, id_tema, id_param_padre FROM f_parametrizacion_all();")
            rows = cursor.fetchall()
        return [Parametrizacion(*row) for row in rows]

    def get_by_tema(self, id_tema: int):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_param, nombre, id_param_padre FROM f_parametrizacion_by_tema(%s);", [id_tema])
            rows = cursor.fetchall()
        return [Parametrizacion(*row) for row in rows]

    def get_estados(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_entidad_federativa, nombre_entidad FROM f_buscar_estados();")
            rows = cursor.fetchall()
        return [Estado(*row) for row in rows]

    def get_instituciones_por_estado(self, id_entidad_federativa: int):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id_institucion, nombre_institucion, nombre_entidad_federativa FROM f_buscar_institucion_por_estado(%s);",
                [id_entidad_federativa]
            )
            rows = cursor.fetchall()
        return [InstitucionPorEstado(*row) for row in rows]

    def get_estados_by_id_user(self, id_usuario: int):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_entidad_federativa, nombre_entidad FROM f_buscar_estados_por_usuario(%s);", [id_usuario])
            rows = cursor.fetchall()
        return [Estado(*row) for row in rows]
