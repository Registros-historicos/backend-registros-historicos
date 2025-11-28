from django.db import connection
from django.db.utils import DatabaseError

def resolve_user_context(id_usuario: int):
    """
    Obtiene datos de contexto del usuario (rol, institución y CEPAT si aplica).
    Para coordinadores con múltiples instituciones, devuelve una lista de IDs
    en `instituciones` y, si son varias, también `instituciones_count`.
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
                print(f"No se encontró contexto para usuario ID={id_usuario}")
                return None

            columns = [col[0] for col in cursor.description]
            context = dict(zip(columns, row))

            if context.get('rol_id') == 35:
                cursor.execute("""
                    SELECT id_institucion 
                    FROM institucion 
                    ORDER BY id_institucion
                """)
                instituciones = [r[0] for r in cursor.fetchall()]
                context['instituciones'] = instituciones
                context['instituciones_count'] = len(instituciones)
                print(f"Admin detectado: acceso a {len(instituciones)} instituciones.")

            # Para coordinadores (rol 36), obtener TODAS sus instituciones
            if context.get('rol_id') == 36:
                cursor.execute(
                    """
                    SELECT id_institucion 
                    FROM institucion 
                    WHERE id_usuario = %s
                    ORDER BY id_institucion
                    """,
                    [id_usuario],
                )

                instituciones = [r[0] for r in cursor.fetchall()]
                context['instituciones'] = instituciones  # lista de IDs

                # Si solo tiene una institución, nos aseguramos de que id_institucion sea esa
                if len(instituciones) == 1:
                    context['id_institucion'] = instituciones[0]

                elif len(instituciones) > 1:
                    # Añadimos el conteo, PERO NO tocamos institucion_nombre
                    context['instituciones_count'] = len(instituciones)

                print(f"Coordinador con {len(instituciones)} instituciones: {instituciones}")
            # Para CePaT (rol 37), obtener TODAS las instituciones de su CePaT
            if context.get('rol_id') == 37:
                id_cepat = context.get("id_cepat")

                if id_cepat:
                    cursor.execute(
                        """
                        SELECT id_institucion
                        FROM institucion
                        WHERE id_cepat = %s
                        ORDER BY id_institucion
                        """,
                        [id_cepat],
                    )
                    instituciones = [r[0] for r in cursor.fetchall()]
                    context['instituciones'] = instituciones

                    # Si solo hay una, también fijamos id_institucion
                    if len(instituciones) == 1:
                        context['id_institucion'] = instituciones[0]
                    else:
                        context['instituciones_count'] = len(instituciones)

                    print(f"CePaT con {len(instituciones)} instituciones: {instituciones}")

            # Limpieza de strings
            for k, v in context.items():
                if isinstance(v, str):
                    context[k] = v.strip()

            print("Contexto usuario:", context)
            return context

    except (DatabaseError, Exception) as e:
        print(f"Error al resolver contexto de usuario {id_usuario}: {str(e)}")
        return None


def get_instituciones_permitidas(id_usuario: int):
    """
    Devuelve la lista de instituciones donde el usuario puede registrar.
    Regla real:
      - CePaT (rol 37): muchas instituciones (todas las del CePaT)
      - Coordinador (rol 36): solo su institución
      - Otros roles: solo su institución
    """
    ctx = resolve_user_context(id_usuario)
    if not ctx:
        return []

    rol_id = ctx.get("rol_id")
    instituciones = ctx.get("instituciones", [])
    id_institucion = ctx.get("id_institucion")
    id_cepat = ctx.get("id_cepat")

    # === CePaT → varias instituciones ===
    if rol_id == 37 and id_cepat:
        return instituciones  # esta lista la llena resolve_user_context()

    # === Coordinador → solo 1 institución ===
    if rol_id == 36:
        return [id_institucion]
    
    if rol_id == 35:
        return instituciones  # Admin puede todas las instituciones

    # === Cualquier otro usuario → solo su institución ===
    return [id_institucion]


def usuario_puede_registrar_en(id_usuario: int, institucion_id: int):
    """
    Valida si el usuario tiene permiso de registrar en esa institución.
    """
    permitidas = get_instituciones_permitidas(id_usuario)
    return institucion_id in permitidas
