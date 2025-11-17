from typing import List, Dict
from django.db import connection


def get_investigadores_por_coordinador_repo(id_usuario: int) -> List[Dict]:
    """
    Llama a la función Postgres f_busca_investigadores_por_coordinador(p_id_usuario)
    y retorna los investigadores asociados a la(s) institución(es) de ese coordinador.

    Args:
        id_usuario: El id_usuario del coordinador.

    Returns:
        Lista de dicts con los datos de los investigadores.
    """
    with connection.cursor() as cursor:
        query = """
                SELECT * \
                FROM public.f_busca_investigadores_por_coordinador(%s) \
                """

        # Pasa el id_usuario como parámetro a la función de Postgres
        cursor.execute(query, [id_usuario])

        # Obtiene los nombres de las columnas que retornó la función
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

    # Convierte los resultados en una lista de diccionarios
    return [dict(zip(cols, r)) for r in rows]