from typing import Optional
from ...domain.entities import Cepat, CepatPatchResult
from ...domain.ports import CepatRepositoryPort
from apps.users.application.selectors.resolve_user_context import resolve_user_context
from django.core.exceptions import PermissionDenied


class CepatCommandsService:
    """
    Servicio para manejar los casos de uso de escritura (Comandos).
    """
    def __init__(self, repo: CepatRepositoryPort):
        self.repo = repo

    def _is_allowed(self, user) -> bool:
        """
        Método auxiliar privado para verificar permisos de Admin (35) o Cepat (37).
        """
        id_usuario = getattr(user, "id", None)
        if not id_usuario:
            return False

        context = resolve_user_context(int(id_usuario))
        if not context:
            return False

        rol_id = context["rol_id"]
        # Solo Admin y Cepat pueden ejecutar comandos
        return rol_id == 35 or rol_id == 37

    def create_cepat(self, user, nombre: str, id_usuario: int) -> Cepat:
        """
        Caso de uso para crear un nuevo Cepat.
        Lanza PermissionDenied si no es Admin (35) o Cepat (37).
        """
        if not self._is_allowed(user):
            raise PermissionDenied("No tiene permiso para crear un Cepat.")

        return self.repo.create(nombre, id_usuario)

    def update_cepat(self, user, cepat_id: int, nombre: str, id_usuario: int) -> Optional[Cepat]:
        """
        Caso de uso para actualizar un Cepat.
        Lanza PermissionDenied si no es Admin (35) o Cepat (37).
        """
        if not self._is_allowed(user):
            raise PermissionDenied("No tiene permiso para actualizar este Cepat.")

        return self.repo.update(cepat_id, nombre, id_usuario)

    def update_cepat_usuario(self, user, cepat_id: int, id_usuario: int) -> Optional[CepatPatchResult]:
        """
        Caso de uso para actualizar solo el usuario de un Cepat (PATCH).
        Lanza PermissionDenied si no es Admin (35) o Cepat (37).
        """
        if not self._is_allowed(user):
            raise PermissionDenied("No tiene permiso para actualizar este Cepat.")

        return self.repo.update_usuario(cepat_id, id_usuario)

    def delete_cepat(self, user, cepat_id: int) -> Optional[Cepat]:
        """
        Caso de uso para eliminar un Cepat.
        Lanza PermissionDenied si no es Admin (35) o Cepat (37).
        """
        if not self._is_allowed(user):
            raise PermissionDenied("No tiene permiso para eliminar este Cepat.")

        return self.repo.delete(cepat_id)