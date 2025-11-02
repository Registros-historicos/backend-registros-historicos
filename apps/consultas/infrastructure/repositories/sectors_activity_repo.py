from typing import List, Dict
from django.db import connection

def get_sectores_por_actividad(user=None) -> List[Dict]:
    """
    Retorna sectores por actividad:
    - Admin (rol 35): función PostgreSQL f_cuenta_registros_por_actividad()
    - CEPAT (rol 37): función PostgreSQL f_cuenta_registros_por_sector_cepat()
    """
    
    # Obtener el rol del usuario (manejando ambos nombres)
    user_role = None
    
    # Buscar en ambos nombres posibles
    if hasattr(user, 'tipo_usuario_param'):
        user_role = user.tipo_usuario_param
    elif hasattr(user, 'tipoo_usuario_param'):
        user_role = user.tipoo_usuario_param
    else:
        return [{
            "sector_nombre": "Error de sistema",
            "actividad_nombre": "Usuario sin rol asignado",
            "total": 0
        }]
    
    # CEPAT: usar función actualizada
    if user_role == 37:
        # Obtener id_cepat de la base de datos
        cepat_id = None
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id_cepat FROM public.cepat WHERE id_usuario = %s", 
                    [user.id]
                )
                result = cursor.fetchone()
                if result:
                    cepat_id = result[0]
                else:
                    return [{
                        "sector_nombre": "Configuración requerida",
                        "actividad_nombre": "Usuario CEPAT necesita asignación a institución",
                        "total": 0
                    }]
        except Exception:
            return [{
                "sector_nombre": "Error de sistema",
                "actividad_nombre": "Problema al cargar configuración",
                "total": 0
            }]
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT nombre_sector, nombre_subsector, cantidad_registros FROM f_cuenta_registros_por_sector_cepat(%s)", 
                    [cepat_id]
                )
                cols = [c[0] for c in cursor.description]
                rows = cursor.fetchall()
            
            if not rows:
                return [{
                    "sector_nombre": "Sin registros",
                    "actividad_nombre": "No hay registros disponibles para esta institución",
                    "total": 0
                }]
            
            resultado = []
            for row in rows:
                resultado.append({
                    "sector_nombre": row[0],
                    "actividad_nombre": row[1], 
                    "total": row[2]
                })
            
            return resultado
            
        except Exception:
            # Fallback a función admin
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT sector_nombre, actividad_nombre, total FROM f_cuenta_registros_por_actividad()")
                    cols = [c[0] for c in cursor.description]
                    rows = cursor.fetchall()
                
                return [dict(zip(cols, r)) for r in rows]
            except Exception:
                return [{
                    "sector_nombre": "Error del sistema",
                    "actividad_nombre": "Error al obtener datos",
                    "total": 0
                }]
    
    # ADMIN y otros roles: función general
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT sector_nombre, actividad_nombre, total FROM f_cuenta_registros_por_actividad()")
            cols = [c[0] for c in cursor.description]
            rows = cursor.fetchall()
        
        datos = [dict(zip(cols, r)) for r in rows]
        
        if not datos:
            return [{
                "sector_nombre": "Sin registros",
                "actividad_nombre": "No hay registros disponibles",
                "total": 0
            }]
        
        return datos
        
    except Exception:
        return [{
            "sector_nombre": "Error del sistema",
            "actividad_nombre": "Error al obtener datos",
            "total": 0
        }]