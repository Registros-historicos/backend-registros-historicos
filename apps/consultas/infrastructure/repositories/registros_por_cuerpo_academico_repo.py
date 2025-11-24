from typing import List, Dict
from django.db import connection


def get_registros_por_cuerpo_academico_repo(id_usuario: int) -> List[Dict]:
    """
    Ejecuta la función f_conteo_registros_por_cuerpo_academico_coordinador.
    Retorna una lista de diccionarios con:
      - nombre_cuerpo_academico
      - total_registros
    """
    with connection.cursor() as cursor:
        query = "SELECT * FROM public.f_conteo_registros_por_cuerpo_academico_coordinador(%s)"
        cursor.execute(query, [id_usuario])
        cols = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    return [dict(zip(cols, row)) for row in rows]
