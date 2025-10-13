from django.db import connection
from apps.parametrizacion.domain.entities import Parametrizacion
from apps.parametrizacion.domain.ports import ParametrizacionRepositoryPort

class ParametrizacionRepository(ParametrizacionRepositoryPort):

    def get_all(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_param, nombre, id_tema, id_param_padre FROM f_parametrizacion_all();")
            rows = cursor.fetchall()
        return [Parametrizacion(*row) for row in rows]

    def get_by_tema(self, id_tema: int):
        with connection.cursor() as cursor:
            cursor.execute("SELECT id_param, nombre, id_tema, id_param_padre FROM f_parametrizacion_by_tema(%s);", [id_tema])
            rows = cursor.fetchall()
        return [Parametrizacion(*row) for row in rows]
