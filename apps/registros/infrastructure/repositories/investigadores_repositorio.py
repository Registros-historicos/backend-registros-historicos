from apps.registros.infrastructure.repositories.pg_utils import run_query


class PostgresInvestigadorRepository:
    """
    Repositorio PostgreSQL para tabla 'investigador' y relación con 'adscripcion'.
    """

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
