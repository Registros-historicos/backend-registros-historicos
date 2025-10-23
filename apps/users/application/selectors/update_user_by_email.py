from typing import Dict, Any, Optional
from apps.users.application.services.user_comands import UserCommandsService
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.domain.entities import Usuario


def update_user(correo: str, data: Dict[str, Any]) -> Optional[Usuario]:
    """
    Selector para actualizar un usuario.
    Este selector traduce la solicitud (correo, data) a lo que
    el UsuarioService espera (user_id, data, new_password).
    """

    # 1. Instanciamos el repositorio (lo usaremos 2+ veces)
    repository = PgUserRepository()

    # 2. PRIMERA LLAMADA A DB: Obtener el usuario actual para sacar su ID
    #    (Necesario porque el service.update_user pide user_id)
    usuario_actual = repository.obtener_por_correo(correo)

    if not usuario_actual:
        # Si el usuario no existe, no podemos actualizar
        return None

    user_id = usuario_actual.id_usuario

    # 3. Extraer la contraseña del diccionario 'data'
    #    (El service la espera como un argumento separado)
    new_password = data.pop('password', None)

    # 4. Instanciar el servicio, inyectando el repositorio
    service = UserCommandsService(repository)

    # 5. Llamar al método del servicio
    #    (Asumiendo que tu service.update_user devuelve None, como en tu ejemplo)
    service.update_user(
        user_id=user_id,
        data=data,
        new_password=new_password
    )

    # 6. SEGUNDA LLAMADA A DB: Obtener el usuario con los datos actualizados
    #    (Necesario porque la View espera el objeto actualizado y el service devolvió None)

    #    Comprobamos si el correo fue parte de la actualización
    correo_actualizado = data.get("correo", correo)

    usuario_actualizado_obj = repository.obtener_por_correo(correo_actualizado)

    return usuario_actualizado_obj