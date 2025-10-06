from typing import List, Dict
from django.db import connection

class StatusRecordsRepository:
    def obtener_conteo_por_estatus(self) -> List[Dict[str, int]]:
        """
        Devuelve todos los estatus del catálogo con su total,
        incluyendo los que tengan total = 0, ordenados por total desc.
        """
        query = """
            WITH counts AS (
                SELECT estatus_param, total
                FROM f_cuenta_registros_por_status()
            )
            SELECT
                p.nombre AS estatus,
                COALESCE(c.total, 0) AS total
            FROM parametrizacion AS p
            LEFT JOIN counts c
            ON c.estatus_param = p.id_param
            WHERE p.id_tema = 7   -- Tema 7 es estatus de solicitud
            ORDER BY total DESC, estatus ASC
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]
