from typing import Dict, Any, Optional
from apps.users.application.services.user_comands import UserCommandsService
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.domain.entities import Usuario


def update_user(correo: str, data: Dict[str, Any]) -> Optional[Usuario]:
    """
    Selector para actualizar un usuario.
    Llama al servicio de comandos y devuelve directamente el usuario actualizado
    que retorna la base de datos.
    """
    repository = PgUserRepository()
    service = UserCommandsService(repository)
    new_password = data.pop('password', None)
    usuario_actualizado = service.update_user(
        correo=correo,
        data=data,
        new_password=new_password
    )
    return usuario_actualizado