from typing import List, Dict
from apps.consultas.infrastructure.repositories.requests_by_type_repo import get_requests_by_type
from apps.users.application.selectors.resolve_user_context import resolve_user_context

def requests_impi() -> List[Dict]:
    """
    Returns requests grouped by type (IMPI).
    """
    return get_requests_by_type("impi")

def requests_indautor() -> List[Dict]:
    """
    Returns requests grouped by type (INDAUTOR).
    """
    return get_requests_by_type("indautor")

from django.db import connection

def requests_by_type_selector(tipo_registro_param: int, user):
    """
    Devuelve los registros agrupados por rama según el tipo de registro (IMPI/INDAUTOR)
    y el rol del usuario:
      - ADMIN → f_cuenta_registros_por_tipo(tipo)
      - CEPAT → f_cuenta_registros_por_tipo_cepat(tipo, id_cepat)
      - Otro → f_cuenta_registros_por_tipo_usuario(id_usuario, tipo) TBD
    """
    rol_id = getattr(user, "rol_id", None) or getattr(user, "id_rol", None)
    id_cepat = getattr(user, "id_cepat", None)
    id_usuario = getattr(user, "id", None)

    with connection.cursor() as cursor:
        context = resolve_user_context(int(id_usuario))
        if not context:
            return []

        rol_id = context["rol_id"]
        id_cepat = context.get("id_cepat")
        id_institucion = context.get("id_institucion")

        if rol_id == 35:
            cursor.execute("SELECT * FROM f_cuenta_registros_por_tipo(%s);", [tipo_registro_param])
        elif rol_id == 37:
            cursor.execute("SELECT * FROM f_cuenta_registros_por_tipo_cepat(%s, %s);", [tipo_registro_param, id_cepat])
        else:
            print ("Usuario otro rol detectado, id_usuario:", id_usuario)
        columns = [col[0] for col in cursor.description]
        data = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return data
