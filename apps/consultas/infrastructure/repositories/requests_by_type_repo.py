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
            p_tipo.nombre AS tipo_registro,
            p_rama.nombre AS rama,
            COUNT(r.id_registro) AS total
        FROM
            f_cuenta_registros_por_tipo_registro() AS f
        JOIN
            parametrizacion AS p_tipo ON p_tipo.id_param = f.tipo_registro_param
        JOIN 
            registro AS r ON r.tipo_registro_param = f.tipo_registro_param
        JOIN
            parametrizacion AS p_rama ON p_rama.id_param = r.rama_param
        WHERE 
            p_tipo.nombre = %s
        GROUP BY
            p_tipo.nombre, 
            p_rama.nombre
        ORDER BY
            total DESC, p_tipo.nombre, p_rama.nombre;
        """, [institucion.upper()])

        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

    return [dict(zip(cols, r)) for r in rows]