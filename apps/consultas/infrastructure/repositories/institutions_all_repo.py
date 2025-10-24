from typing import List, Dict
from django.db import connection

class InstitutionsAllRepository:
    """
    Repositorio para obtener todas las instituciones con total de registros.
    """
    def obtener_instituciones_all(self) -> List[Dict]:
        query = """
            SELECT id_institucion, institucion_nombre, total, tipo_institucion
            FROM f_cuenta_registros_por_institucion_all()
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]