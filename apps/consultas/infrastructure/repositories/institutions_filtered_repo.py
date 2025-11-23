from typing import List, Dict
from django.db import connection


class InstitutionsFilteredRepository:
    """
    Repositorio para obtener instituciones filtradas por tipo.
    """
    
    def obtener_instituciones_por_tipo(self, tipo_institucion: int) -> List[Dict]:
        """
        Obtiene TODAS las instituciones de un tipo específico (sin filtro de CEPAT).
        Para usuarios ADMIN.
        """
        query = """
            SELECT 
                id_institucion,
                institucion_nombre,
                total
            FROM f_cuenta_registros_por_institucion_filtrado(%s)
            ORDER BY total DESC
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [tipo_institucion])
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]
    
    def obtener_instituciones_por_tipo_y_cepat(self, tipo_institucion: int, id_cepat: int) -> List[Dict]:
        """
        Obtiene instituciones de un tipo específico FILTRADAS por CEPAT.
        Para usuarios CEPAT.
        """
        query = """
            SELECT 
                f.id_institucion,
                f.institucion_nombre,
                f.total
            FROM f_cuenta_registros_por_institucion_filtrado(%s) f
            JOIN institucion i ON i.id_institucion = f.id_institucion
            WHERE i.id_cepat = %s
            ORDER BY f.total DESC
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [tipo_institucion, id_cepat])
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]
    
    def obtener_instituciones_por_tipo_y_lista(self, tipo_institucion: int, ids_instituciones: List[int]) -> List[Dict]:
        """
        Obtiene instituciones de un tipo específico FILTRADAS por una lista de IDs.
        Para usuarios COORDINADOR con múltiples instituciones.
        """
        if not ids_instituciones:
            return []
        
        placeholders = ','.join(['%s'] * len(ids_instituciones))
        
        query = f"""
            SELECT 
                f.id_institucion,
                f.institucion_nombre,
                f.total
            FROM f_cuenta_registros_por_institucion_filtrado(%s) f
            WHERE f.id_institucion IN ({placeholders})
            ORDER BY f.total DESC
        """
        
        params = [tipo_institucion] + ids_instituciones
        
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]