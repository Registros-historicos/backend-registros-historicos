from apps.investigadores.domain.entities import Investigador, Adscripcion
from apps.investigadores.domain.ports import InvestigadorRepositoryPort
from .pg_utils import call_function


class InvestigadorRepository(InvestigadorRepositoryPort):
    """
    Implementación del repositorio para la entidad Investigador,
    usando funciones Postgres en lugar del ORM.
    """

    def crear(self, investigador: Investigador) -> Investigador:
        result = call_function(
            """
            SELECT * FROM f_crear_investigador(%s, %s, %s, %s, %s, %s);
            """,
            [
                investigador.nombre,
                investigador.ape_pat,
                investigador.ape_mat,
                investigador.curp,
                investigador.sexo_param,
                investigador.tipo_investigador_param,
            ],
        )
        return Investigador(**result[0]) if result else None

    def actualizar(self, investigador: Investigador) -> Investigador:
        result = call_function(
            """
            SELECT * FROM f_actualizar_investigador(%s, %s, %s, %s, %s, %s, %s);
            """,
            [
                investigador.id_investigador,
                investigador.nombre,
                investigador.ape_pat,
                investigador.ape_mat,
                investigador.curp,
                investigador.sexo_param,
                investigador.tipo_investigador_param,
            ],
        )
        return Investigador(**result[0]) if result else None

    def eliminar(self, id_investigador: int) -> None:
        call_function("SELECT f_eliminar_investigador(%s);", [id_investigador])

    def crear_adscripcion(self, adscripcion: Adscripcion) -> Adscripcion:
        result = call_function(
            """
            SELECT * FROM f_insertar_adscripcion(
                %s, %s, %s,
                CAST(%s AS date),
                CAST(%s AS date),
                %s, %s
            );
            """,
            [
                adscripcion.departamento_param,
                adscripcion.programa_educativo_param,
                adscripcion.cuerpo_academico_param,
                adscripcion.fec_ini,
                adscripcion.fec_fin,
                adscripcion.id_institucion,
                adscripcion.id_investigador,
            ],
        )
        return result[0] if result else None


    def get_by_curp(self, curp: str):
        """Obtiene un investigador por CURP."""
        query = """
            SELECT i.id_investigador, i.curp, i.nombre, i.ape_pat, i.ape_mat,
                   i.sexo_param, i.tipo_investigador_param
            FROM investigador i
            WHERE i.curp = %s;
        """
        return run_query(query, [curp], fetchone=True)

