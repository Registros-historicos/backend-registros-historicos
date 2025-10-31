from django.db import connection
from typing import List, Dict
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def registros_por_periodo_selector(fecha_inicio: str, fecha_fin: str, user) -> List[Dict[str, int]]:
    """
    Retorna los registros agrupados por año, mes y tipo de registro para un rango de fechas.
    Aplica contexto según rol del usuario:
      - rol 35: f_cuenta_registros_por_periodo(%s, %s)
      - rol 36: f_cuenta_registros_por_periodo_coordinador(%s, %s, %s)  # filtra por id_institucion
      - rol 37: f_cuenta_registros_por_periodo_cepat(%s, %s, %s)
      - otro: []
    """
    id_usuario = getattr(user, "id", None)

    with connection.cursor() as cursor:
        context = resolve_user_context(int(id_usuario))
        if not context:
            return []
        rol_id = context.get("rol_id")
        id_cepat = context.get("id_cepat")
        id_institucion = context.get("id_institucion")

        if rol_id == 35:
            cursor.execute("SELECT * FROM f_cuenta_registros_por_periodo(%s, %s)", [fecha_inicio, fecha_fin])
        elif rol_id == 36:
            cursor.execute("SELECT * FROM f_cuenta_registros_por_periodo_coordinador(%s, %s, %s)", [fecha_inicio, fecha_fin, id_institucion])
        elif rol_id == 37:
            cursor.execute("SELECT * FROM f_cuenta_registros_por_periodo_cepat(%s, %s, %s)", [fecha_inicio, fecha_fin, id_cepat])
        else:
            return []

        columnas = [col[0] for col in cursor.description]
        filas = cursor.fetchall()

    datos = [dict(zip(columnas, fila)) for fila in filas]
    datos_ordenados = sorted(datos, key=lambda x: (x["anio"], x["mes"]))
    return datos_ordenados
