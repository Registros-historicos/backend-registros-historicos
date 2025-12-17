from apps.registros.infrastructure.repositories.pg_utils import run_query
from .pg_utils import call_function



class PostgresInvestigadorRepository:
    """
    Repositorio PostgreSQL para tabla 'investigador' y relación con 'adscripcion'.
    """

    def list_all_investigadores(self):
        """Obtiene todos los investigadores."""
        query = """
            SELECT i.id_investigador, i.curp, i.nombre, i.ape_pat, i.ape_mat,
                   i.sexo_param, i.tipo_investigador_param
            FROM investigador i;
        """
        return run_query(query)

    def list_curps(self):

        """Obtiene todas las CURP de investigadores."""
        query = "SELECT * FROM obtener_curp();"

        print("Ejecutando query para listar CURPs de investigadores.")
        print(call_function(query))
        return call_function(query)

    def get_by_curp(self, curp: str):
        """Obtiene un investigador por CURP."""
        query = """
            SELECT i.id_investigador, i.curp, i.nombre, i.ape_pat, i.ape_mat,
                   i.sexo_param, i.tipo_investigador_param
            FROM investigador i
            WHERE i.curp = %s;
        """
        return run_query(query, [curp], fetchone=True)

    def vincular_adscripcion(self, id_investigador: int, adscripcion_data: dict):
        """Crea una adscripción si no existe una activa (opcional)."""
        query = """
            INSERT INTO adscripcion (
                departamento_param, programa_educativo_param,
                cuerpo_academico_param, fec_ini, fec_fin,
                id_institucion, id_investigador
            )
            VALUES (
                %(departamento_param)s, %(programa_educativo_param)s,
                %(cuerpo_academico_param)s, %(fec_ini)s, %(fec_fin)s,
                %(id_institucion)s, %(id_investigador)s
            )
            ON CONFLICT DO NOTHING;
        """
        run_query(query, adscripcion_data)

    def desvincular_adscripcion(self, id_investigador: int):
        """Desvincula (elimina) la adscripción activa de un investigador."""
        query = """
            DELETE FROM adscripcion
            WHERE id_investigador = %s
              AND fec_fin IS NULL;
        """
        run_query(query, [id_investigador])
