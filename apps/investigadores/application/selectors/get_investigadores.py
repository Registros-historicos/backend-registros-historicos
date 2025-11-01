from apps.investigadores.infrastructure.repositories.pg_utils import call_function
from apps.investigadores.domain.entities import Investigador


def get_all_investigadores():
    """
    Obtiene la lista de todos los investigadores registrados
    desde la tabla 'investigador' usando las columnas reales
    de la base de datos SARPITH.
    """
    result = call_function("""
        SELECT 
            id_investigador,
            nombre,
            ape_pat,
            ape_mat,
            curp,
            sexo_param,
            tipo_investigador_param
        FROM public.investigador
        ORDER BY id_investigador;
    """)
    return [Investigador(**row) for row in result]
