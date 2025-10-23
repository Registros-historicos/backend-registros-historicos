from typing import Optional
from django.contrib.auth.hashers import make_password
from apps.users.domain.entities import Usuario
from apps.users.domain.ports import UserRepositoryPort

class UserCommandsService:
    def __init__(self, repo: UserRepositoryPort):
        self.repo = repo

    def create_user(self, data: dict, raw_password: str) -> int:
        def create_user(self, data: dict, raw_password: str) -> int:
            user = Usuario(
                id_usuario=None,
                nombre=data["nombre"],
                ape_pat=data["ape_pat"],
                ape_mat=data.get("ape_mat"),
                url_foto=data.get("url_foto"),
                correo=data["correo"],
                telefono=data.get("telefono"),
                tipo_usuario_param=data["tipo_usuario_param"],
                estatus=data.get("estatus", 24),
            )
            pwd_hash = make_password(raw_password)
            return self.repo.create(user, pwd_hash)

    def update_user( self, correo: str, data: dict, new_password: Optional[str] = None ) -> Optional[Usuario]:
        """
        Construye el objeto Usuario a partir de los datos y llama al repositorio
        para actualizarlo, devolviendo el objeto actualizado.
        """
        user = Usuario(
            id_usuario=None,
            nombre=data.get("nombre"),
            ape_pat=data.get("ape_pat"),
            ape_mat=data.get("ape_mat"),
            url_foto=data.get("url_foto"),
            correo=data.get("correo", correo),
            telefono=data.get("telefono"),
            tipo_usuario_param=data.get("tipo_usuario_param"),
            estatus=data.get("estatus"),
        )
        pwd_hash = make_password(new_password) if new_password else None
        return self.repo.update(user, pwd_hash)

    def delete_user(self, user_id: int) -> None:
        self.repo.delete(user_id)
