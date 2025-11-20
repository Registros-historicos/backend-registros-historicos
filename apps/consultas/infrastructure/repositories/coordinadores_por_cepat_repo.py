from typing import List, Dict
from django.db import connection


def get_coordinadores_por_usuario_cepat_repo(id_usuario_sesion: int) -> List[Dict]:
    """
    Ejecuta la función f_obtener_coordinadores_por_usuario_cepat.
    """
    with connection.cursor() as cursor:
        query = "SELECT * FROM public.f_obtener_coordinadores_por_usuario_cepat(%s)"
        cursor.execute(query, [id_usuario_sesion])
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

    return [dict(zip(cols, r)) for r in rows]