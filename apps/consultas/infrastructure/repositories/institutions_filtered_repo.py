from typing import List, Dict
from django.db import connection

class InstitutionsFilteredRepository:
    """
    Repositorio para obtener instituciones filtradas por tipo.
    """
    def obtener_instituciones_por_tipo(self, tipo_institucion: int) -> List[Dict]:
        query = """
            SELECT 
                id_institucion,
                institucion_nombre,
                total
            FROM f_cuenta_registros_por_institucion_filtrado(%s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [tipo_institucion])
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]