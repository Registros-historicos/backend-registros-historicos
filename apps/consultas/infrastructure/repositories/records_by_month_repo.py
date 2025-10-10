from typing import List, Dict
from django.db import connection

class MonthRecordsRepository:
    """
    Repositorio para obtener conteo de registros por mes.
    """
    def obtener_conteo_por_mes(self, anio: int) -> List[Dict[str, int]]:
        query = """
            SELECT DISTINCT mes, total
            FROM f_cuenta_registros_por_mes(%s)
            ORDER BY mes
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [anio])
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]