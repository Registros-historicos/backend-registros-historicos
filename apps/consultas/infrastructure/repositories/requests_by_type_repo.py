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
        cursor.execute("""
            SELECT 
                p.nombre AS rama,
                f.total
            FROM f_cuenta_registros_por_tipo_registro() f
            JOIN parametrizacion AS p ON f.tipo_registro_param = p.id_param
            ORDER BY total DESC, p.nombre;
        """, [institucion.upper()])

        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

    return [dict(zip(cols, r)) for r in rows]