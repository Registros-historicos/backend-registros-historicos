from typing import List, Dict
from django.db import connection

def get_top10_entidades() -> List[Dict]:
    """
    Llama a la función Postgres f_cuenta_registros_por_entidad_top10()
    y retorna una lista de dicts con keys:
    ent_federativa_param, entidad_nombre, total
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            select ent_federativa_param, entidad_nombre, total
            from f_cuenta_registros_por_entidad_top10()
        """)
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
    return [dict(zip(cols, r)) for r in rows]

