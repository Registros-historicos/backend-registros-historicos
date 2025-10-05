from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository

def disable_record(id_registro: int):
    """
    Selector para deshabilitar un registro.
    """
    repo = PostgresRegistroRepository()
    return repo.deshabilitar(id_registro)
