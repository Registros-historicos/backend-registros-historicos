from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository

def enable_record(id_registro: int):
    """
    Selector para habilitar un registro.
    """
    repo = PostgresRegistroRepository()
    return repo.habilitar(id_registro)
