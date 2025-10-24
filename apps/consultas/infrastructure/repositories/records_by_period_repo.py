from django.db import connection
from typing import List, Dict


class RecordsByPeriodRepository:
    """
    Repositorio para obtener conteo de registros por periodo.
    """
    def obtener_registros_por_periodo(self, fecha_inicio: str, fecha_fin: str) -> List[Dict[str, int]]:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM f_cuenta_registros_por_periodo(%s, %s)",
                [fecha_inicio, fecha_fin]
            )
            columnas = [col[0] for col in cursor.description]
            filas = cursor.fetchall()
        return [dict(zip(columnas, fila)) for fila in filas]
