from typing import List, Dict
from django.db import connection

def get_top10_instituciones() -> List[Dict]:
    """
    Llama a la función Postgres f_cuenta_registros_por_institucion_top10()
    y retorna una lista de dicts con keys:
    id_institucion, institucion_nombre, total
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            select id_institucion, institucion_nombre, total
            from f_cuenta_registros_por_institucion_top10()
        """)
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
    return [dict(zip(cols, r)) for r in rows]

def get_instituciones_por_cepat(id_cepat: int, limit: int = None) -> List[Dict]:
    """
    Llama a la función Postgres f_cuenta_registros_por_institucion_cepat(p_id_cepat)
    y retorna una lista de instituciones filtradas por CEPAT.
    
    Args:
        id_cepat: ID del CEPAT para filtrar
        limit: Opcional, limita los resultados (ej. 10 para top10)
    
    Returns:
        Lista de dicts con keys: id_institucion, institucion_nombre, tipo_institucion, total
    """
    with connection.cursor() as cursor:
        query = """
            SELECT id_institucion, institucion_nombre, tipo_institucion, total
            FROM f_cuenta_registros_por_institucion_cepat(%s)
        """
        
        # Si queremos limitar (ej. Top 10), agregamos LIMIT
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query, [id_cepat])
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
    
    return [dict(zip(cols, r)) for r in rows]
