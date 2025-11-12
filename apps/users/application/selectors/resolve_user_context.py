from django.db import connection
from django.db.utils import DatabaseError

def resolve_user_context(id_usuario: int):
    """
    Obtiene datos de contexto del usuario (rol, institución y CEPAT si aplica).
    Para coordinadores con múltiples instituciones, devuelve una lista de IDs.
    """
    if not isinstance(id_usuario, int):
        raise ValueError("El parámetro id_usuario debe ser un número entero.")

    query = """
        SELECT 
            u.id_usuario,
            u.correo,
            u.tipo_usuario_param AS rol_id,
            r.nombre AS rol_nombre,
            COALESCE(i_cepat.id_institucion, i_coord.id_institucion) AS id_institucion,
            COALESCE(i_cepat.nombre, i_coord.nombre) AS institucion_nombre,
            c.id_cepat,
            c.nombre AS cepat_nombre
        FROM usuario u
        LEFT JOIN parametrizacion r ON r.id_param = u.tipo_usuario_param
        LEFT JOIN cepat c ON c.id_usuario = u.id_usuario
        LEFT JOIN institucion i_cepat ON i_cepat.id_cepat = c.id_cepat
        LEFT JOIN institucion i_coord ON i_coord.id_usuario = u.id_usuario
        WHERE u.id_usuario = %s
        ORDER BY COALESCE(i_cepat.nombre, i_coord.nombre)
        LIMIT 1;
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(query, [id_usuario])
            row = cursor.fetchone()

            if not row:
                print(f"⚠️ No se encontró contexto para usuario ID={id_usuario}")
                return None

            columns = [col[0] for col in cursor.description]
            context = dict(zip(columns, row))
            
            # Para coordinadores (rol 36), obtener TODAS sus instituciones
            if context.get('rol_id') == 36:
                cursor.execute("""
                    SELECT id_institucion 
                    FROM institucion 
                    WHERE id_usuario = %s
                    ORDER BY id_institucion
                """, [id_usuario])
                
                instituciones = [row[0] for row in cursor.fetchall()]
                context['instituciones'] = instituciones  # Lista de IDs de instituciones
                
                # Actualizar el nombre para mostrar cantidad
                if len(instituciones) > 1:
                    context['institucion_nombre'] = f"{len(instituciones)} instituciones"
                
                print(f"✅ Coordinador con {len(instituciones)} instituciones: {instituciones}")
            
            for k, v in context.items():
                if isinstance(v, str):
                    context[k] = v.strip()

            print("✅ Contexto usuario:", context)
            return context

    except (DatabaseError, Exception) as e:
        print(f"❌ Error al resolver contexto de usuario {id_usuario}: {str(e)}")
        return None