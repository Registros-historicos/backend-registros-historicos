from typing import List, Dict
from django.db import connection

class StatusRecordsRepository:
    """
    Repositorio para obtener conteo de registros por estatus de solicitud.
    """

    def obtener_conteo_por_estatus(self) -> List[Dict[str, int]]:
        """
        Conteo global por estatus (rol 35 - admin).
        Incluye estatus con total = 0, ordenados desc.
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
            ORDER BY total DESC, estatus ASC;
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]

    def obtener_conteo_por_estatus_institucion(self, id_institucion: int) -> List[Dict[str, int]]:
        """
        Conteo por estatus para una institución específica (rol 36 - coordinador).
        """
        query = """
            WITH counts AS (
                SELECT estatus_param, total
                FROM f_cuenta_registros_por_status_institucion(%s)
            )
            SELECT
                p.nombre AS estatus,
                COALESCE(c.total, 0) AS total
            FROM parametrizacion AS p
            LEFT JOIN counts c
                ON c.estatus_param = p.id_param
            WHERE p.id_tema = 7
            ORDER BY total DESC, estatus ASC;
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [id_institucion])
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]

    def obtener_conteo_por_estatus_cepat(self, id_cepat: int) -> List[Dict[str, int]]:
        """
        Conteo por estatus para todos los institutos asociados a un CEPAT (rol 37).
        """
        query = """
            WITH counts AS (
                SELECT estatus_param, total
                FROM f_cuenta_registros_por_status_cepat(%s)
            )
            SELECT
                p.nombre AS estatus,
                COALESCE(c.total, 0) AS total
            FROM parametrizacion AS p
            LEFT JOIN counts c
                ON c.estatus_param = p.id_param
            WHERE p.id_tema = 7
            ORDER BY total DESC, estatus ASC;
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [id_cepat])
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]
