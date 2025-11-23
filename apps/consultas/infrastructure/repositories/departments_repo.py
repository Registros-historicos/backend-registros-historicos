from typing import List, Dict
from django.db import connection


class DepartmentsRepository:
    """
    Repositorio para obtener conteos de registros por departamento.
    """
    
    def obtener_departamentos_all(self) -> List[Dict]:
        """
        Conteo global de todos los departamentos (para Admin).
        """
        query = """
            SELECT 
                departamento_param,
                nombre_departamento,
                total
            FROM f_cuenta_registros_por_departamento()
            ORDER BY total DESC
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]
    
    def obtener_departamentos_por_institucion(self, id_institucion: int) -> List[Dict]:
        """
        Conteo de departamentos filtrado por UNA institución (para Coordinador con 1 institución).
        """
        query = """
            SELECT 
                departamento_param,
                nombre_departamento,
                total
            FROM f_cuenta_registros_por_departamento_institucion(%s)
            ORDER BY total DESC
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [id_institucion])
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]
    
    def obtener_departamentos_por_instituciones(self, ids_instituciones: List[int]) -> List[Dict]:
        """
        Conteo de departamentos filtrado por MÚLTIPLES instituciones (para Coordinador con varias).
        """
        if not ids_instituciones:
            return []
        
        placeholders = ','.join(['%s'] * len(ids_instituciones))
        
        query = f"""
            SELECT 
                a.departamento_param,
                p.nombre AS nombre_departamento,
                COUNT(DISTINCT r.id_registro)::BIGINT AS total
            FROM registro r
            JOIN registro_investigador ri ON ri.id_registro = r.id_registro
            JOIN adscripcion a ON a.id_investigador = ri.id_investigador
            JOIN parametrizacion p ON p.id_param = a.departamento_param
            WHERE a.id_institucion IN ({placeholders})
            GROUP BY a.departamento_param, p.nombre
            ORDER BY total DESC
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, ids_instituciones)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]