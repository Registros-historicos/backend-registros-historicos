from typing import List, Dict
from django.db import connection


def get_registros_por_programa_repo(id_usuario: int) -> List[Dict]:
    """
    Ejecuta la función f_conteo_registros_por_programa_coordinador.
    """
    with connection.cursor() as cursor:
        query = "SELECT * FROM public.f_conteo_registros_por_programa_coordinador(%s)"
        cursor.execute(query, [id_usuario])
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

    return [dict(zip(cols, r)) for r in rows]