from typing import Dict

from apps.registros.application.services.registros_commands import RegistroService
from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository


def create_new_record(data: Dict) -> Dict:
    """
       Selector para crear un registro usando el repositorio.
       """
    service = RegistroService(PostgresRegistroRepository())
    return service.crear_registro(data)
