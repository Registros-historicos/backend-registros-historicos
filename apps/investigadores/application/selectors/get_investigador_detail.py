from django.db import connection
from apps.investigadores.domain.entities import Investigador

def get_investigador_detail(id_investigador: int) -> Investigador | None:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT 
                id_investigador,
                nombre,
                ape_pat,
                ape_mat,
                curp,
                sexo_param,
                tipo_investigador_param
            FROM public.investigador
            WHERE id_investigador = %s;
        """, [id_investigador])

        row = cursor.fetchone()
        if not row:
            return None

        columns = [col[0] for col in cursor.description]
        data = dict(zip(columns, row))

        return Investigador(**data)
