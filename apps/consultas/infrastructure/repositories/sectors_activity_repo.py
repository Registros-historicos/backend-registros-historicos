from typing import List, Dict
from django.db import connection


def get_sectores_por_actividad() -> List[Dict]:
    """
    Llama a la función Postgres f_cuenta_registros_por_actividad()
    y retorna una lista de dicts con keys:
    tipo_sector_param, sector_nombre, total
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tipo_sector_param, sector_nombre, total
            FROM f_cuenta_registros_por_actividad()
        """)
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
    return [dict(zip(cols, r)) for r in rows]