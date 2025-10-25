from typing import Protocol, Optional, List
from .entities import Usuario


class UserRepositoryPort(Protocol):

    def insertar(self, usuario: 'Usuario', pwd_hash: str) -> Optional['Usuario']:
        """ Llama a f_inserta_usuario """
        ...

    def actualizar(self, correo: str, usuario: 'Usuario', pwd_hash: Optional[str]) -> 'Usuario':
        """ Llama a f_actualiza_usuario_por_correo """
        ...

    def habilitar(self, correo: str, estatus_activo: int) -> Optional['Usuario']:
        """ Llama a f_habilita_usuario """
        ...

    def deshabilitar(self, correo: str, estatus_inactivo: int) -> Optional['Usuario']:
        """ Llama a f_deshabilita_usuario """
        ...

    def buscar_todos_usuario(self) -> List['Usuario']:
        """ Llama a f_buscar_todos_usuario """
        ...

    def obtener_por_correo(self, correo: str) -> Optional['Usuario']:
        """ Llama a f_busca_usuario_por_correo_no_login """
        ...

    def obtener_por_correo_login(self, correo: str) -> Optional[tuple['Usuario', str]]:
        """ Llama a f_busca_usuario_por_correo (para login) """
        ...

    def obtener_por_tipo(self, tipo: int) -> Optional['Usuario']:
        """ Llama a f_busca_usuario_por_tipo_usuario """
        ...