from apps.registros.domain.entities import Registro
from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository


def update_records(id_registro: int, data: dict) -> Registro:
    """
    Selector para actualizar un registro usando el repositorio.
    """
    repo = PostgresRegistroRepository()
    registro = Registro(**data)
    return repo.actualizar(id_registro, registro)
