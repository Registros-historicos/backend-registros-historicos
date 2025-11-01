from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository
from apps.registros.infrastructure.repositories.investigadores_repositorio import PostgresInvestigadorRepository

repo_registro = PostgresRegistroRepository()
repo_investigador = PostgresInvestigadorRepository()


def add_investigador_to_registro(curp: str, investigador_data: dict, no_expediente: str):
    """
    Vincula un investigador existente (por CURP) a un registro,
    usando su id_investigador en la tabla registro_investigador.
    """
    investigador = repo_investigador.get_by_curp(curp)
    if not investigador:
        print(f"⚠️ CURP {curp} no encontrado, se omite vinculación.")
        return None

    registro = repo_registro.get_by_expediente(no_expediente)
    if not registro:
        print(f"⚠️ Registro con expediente {no_expediente} no encontrado.")
        return None

    id_investigador = investigador["id_investigador"]
    repo_registro.vincular_investigador(registro["id_registro"], id_investigador)
    print(f"✅ Vinculado investigador {id_investigador} → registro {registro['id_registro']}")
