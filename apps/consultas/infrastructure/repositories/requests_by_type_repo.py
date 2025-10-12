from typing import List, Dict
from django.db import connection

def get_requests_by_type(institucion: str) -> List[Dict]:
    """
    Llama a la función Postgres f_cuenta_registros_por_tipo_registro()
    Filtra los resultados por institución (IMPI o INDAUTOR)
    y realiza JOIN con la tabla parametrizacion para mostrar el nombre del tipo.
    Retorna una lista de dicts con keys:
    tipo_registro_param, tipo_nombre, total
    """
    with connection.cursor() as cursor:
        tipo_map = {
            'IMPI': 44,
            'INDAUTOR': 45
        }
        tipo_id = tipo_map.get(institucion.upper())
        if not tipo_id:
            raise ValueError(f"Institución desconocida: {institucion}")

        cursor.execute("""
            SELECT 
                tipo_registro_nombre as tipo_registro,
                rama_nombre as rama,
                total
            FROM f_cuenta_registros_por_tipo(%s);

        """, [tipo_id])

        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

    return [dict(zip(cols, r)) for r in rows]