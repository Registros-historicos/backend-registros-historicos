from typing import List, Dict
from django.db import connection


class ProgramsEducationalRepository:
    
    def obtener_programas_all(self) -> List[Dict]:
        """
        Conteo global de todos los programas educativos
        """
        query = """
            SELECT 
                programa_educativo_param,
                nombre_programa_educativo,
                total
            FROM f_cuenta_registros_por_programa_educativo()
            ORDER BY total DESC
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]
    
    def obtener_programas_por_institucion(self, id_institucion: int) -> List[Dict]:
        """
        Conteo por UNA institución específica
        """
        query = """
            SELECT 
                a.programa_educativo_param,
                p.nombre AS nombre_programa_educativo,
                COUNT(DISTINCT r.id_registro)::BIGINT AS total
            FROM registro r
            JOIN registro_investigador ri ON ri.id_registro = r.id_registro
            JOIN adscripcion a ON a.id_investigador = ri.id_investigador
            JOIN parametrizacion p ON p.id_param = a.programa_educativo_param
            WHERE a.id_institucion = %s
            GROUP BY a.programa_educativo_param, p.nombre
            ORDER BY total DESC;
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [id_institucion])
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]
    
    def obtener_programas_por_instituciones(self, ids_instituciones: List[int]) -> List[Dict]:
        """
        Conteo por MÚLTIPLES instituciones - suma total de todas
        """
        if not ids_instituciones:
            return []
        
        placeholders = ','.join(['%s'] * len(ids_instituciones))
        
        query = f"""
            SELECT 
                a.programa_educativo_param,
                p.nombre AS nombre_programa_educativo,
                COUNT(DISTINCT r.id_registro)::BIGINT AS total
            FROM registro r
            JOIN registro_investigador ri ON ri.id_registro = r.id_registro
            JOIN adscripcion a ON a.id_investigador = ri.id_investigador
            JOIN parametrizacion p ON p.id_param = a.programa_educativo_param
            WHERE a.id_institucion IN ({placeholders})
            GROUP BY a.programa_educativo_param, p.nombre
            ORDER BY total DESC;
        """
        
        with connection.cursor() as cursor:
            cursor.execute(query, ids_instituciones)
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]
    
    def obtener_programas_por_cepat(self, id_cepat: int) -> List[Dict]:
        """
        Conteo por CEPAT - incluye todas las instituciones del CEPAT
        """
        query = """
            SELECT 
                programa_educativo_param,
                nombre_programa_educativo,
                total
            FROM f_cuenta_registros_por_programa_educativo_cepat(%s)
            ORDER BY total DESC
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [id_cepat])
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(cols, r)) for r in rows]