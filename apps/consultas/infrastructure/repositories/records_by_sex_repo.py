from typing import List, Dict
from django.db import connection

class SexRecordsRepository:
    """ 
    Repositorio para obtener conteo de registros por sexo de investigador.
    """
    def obtener_conteo_por_sexo(self) -> List[Dict[str, int]]:
        query = """ 
            WITH counts AS (
                SELECT sexo_param, total
                FROM f_cuenta_registros_por_sexo_investigador()
            )
            SELECT 
                p.nombre AS sexo,
                COALESCE(c.total, 0) AS total
            FROM parametrizacion AS p
            LEFT JOIN counts c
                ON c.sexo_param = p.id_param
            WHERE p.id_tema = 1
            ORDER BY total DESC, sexo ASC
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]