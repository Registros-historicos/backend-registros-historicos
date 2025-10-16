from typing import List, Dict
from django.db import connection

class EconomicSectorsRepository:
    """ 
    Repositorio para obtener conteo de registros por sector económico.
    """

    def obtener_conteo_por_sector(self) -> List[Dict]:
        """
        Llama a la función Postgres f_cuenta_registros_por_sectores(),
        la une con la tabla parametrización para obtener los nombres legibles
        y ordena el resultado por el total de forma descendente. 
        """
        query = """ 
            SELECT
                p.nombre AS sector,
                t.total
            FROM
                f_cuenta_registros_por_sectores() AS t
            INNER JOIN
                parametrizacion AS p ON t.tipo_sector_param = p.id_param
            ORDER BY
                t.total DESC;
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            cols = [c[0] for c in cursor.description]
            return [
                dict(zip(cols, r)) 
                for r in cursor.fetchall()
            ]
