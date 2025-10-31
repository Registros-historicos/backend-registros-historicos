from typing import List, Dict
from django.db import connection
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def registros_por_mes_selector(anio: int, user) -> List[Dict[str, int]]:
    """
    Selector para obtener conteo de registros por mes en un año específico.
    Aplica contexto según rol del usuario:
      - rol 35 (ADMIN): f_cuenta_registros_por_mes(%s)
      - rol 36 (COORDINADOR): f_cuenta_registros_por_mes_coordinador(%s, %s)  # filtra por id_institucion
      - rol 37 (CEPAT): f_cuenta_registros_por_mes_cepat(%s, %s)
      - otro: devuelve lista vacía

    Args:
        anio: Año para filtrar los registros
        user: usuario (request.user) para resolver contexto

    Returns:
        Lista de diccionarios con mes y total de registros
    """
    rol_id = getattr(user, "rol_id", None) or getattr(user, "id_rol", None)
    id_usuario = getattr(user, "id", None)

    with connection.cursor() as cursor:
        context = resolve_user_context(int(id_usuario))
        if not context:
            return []

        rol_id = context.get("rol_id")
        id_cepat = context.get("id_cepat")
        id_institucion = context.get("id_institucion")

        if rol_id == 35:
            cursor.execute("SELECT DISTINCT mes, total FROM f_cuenta_registros_por_mes(%s) ORDER BY mes", [anio])
        elif rol_id == 36:
            cursor.execute("SELECT DISTINCT mes, total FROM f_cuenta_registros_por_mes_coordinador(%s, %s) ORDER BY mes", [anio, id_institucion])
        elif rol_id == 37:
            cursor.execute("SELECT DISTINCT mes, total FROM f_cuenta_registros_por_mes_cepat(%s, %s) ORDER BY mes", [anio, id_cepat])
        else:
            return []

        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
    return [dict(zip(cols, r)) for r in rows]
