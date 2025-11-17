from typing import List, Dict
from django.db import connection


def get_usuarios_por_estados_cepat_repo(id_usuario: int) -> List[Dict]:
    """
    Llama a la función Postgres f_buscar_usuarios_por_estados_de_cepat(p_id_usuario)

    Args:
        id_usuario: ID del usuario CEPAT.

    Returns:
        Lista de diccionarios con la información de los usuarios (coordinadores)
        que se encuentran en los estados gestionados por este CEPAT.
    """
    with connection.cursor() as cursor:
        query = """
                SELECT * \
                FROM public.f_buscar_usuarios_por_estados_de_cepat(%s) \
                """
        cursor.execute(query, [id_usuario])

        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

    return [dict(zip(cols, r)) for r in rows]