from typing import List, Dict
from django.db import connection

class FederalEntitiesAllRepository:
    """
    Obtener todas las entidades federativas con todos de registros.
    """
    def obtener_entidades_all(self) -> List[Dict]:
        query = """
            SELECT ent_federativa_param, entidad_nombre, total
            FROM f_cuenta_registros_por_entidad_all()
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]