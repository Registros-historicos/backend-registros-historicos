from apps.investigadores.infrastructure.repositories.pg_utils import call_function
from apps.investigadores.domain.entities import Adscripcion



def get_adscripciones_by_investigador(id_investigador: int):
    """
    Obtiene todas las adscripciones de un investigador por su ID.
    """
    result = call_function("""
        SELECT 
            a.id_adscripcion,
            a.id_investigador,
            a.id_institucion,
            a.departamento_param,
            a.programa_educativo_param,
            a.cuerpo_academico_param,
            a.fec_ini,
            a.fec_fin
        FROM public.adscripcion AS a
        WHERE a.id_investigador = %s
        ORDER BY a.fec_ini DESC;
    """, [id_investigador])

    return [Adscripcion(**row) for row in result]
