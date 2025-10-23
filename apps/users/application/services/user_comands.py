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

    def update_user(self, user_id: int, data: dict, new_password: Optional[str] = None) -> None:
        user = Usuario(
            id_usuario=user_id,
            nombre=data["nombre"],
            ape_pat=data["ape_pat"],
            ape_mat=data.get("ape_mat"),
            url_foto=data.get("url_foto"),
            correo=data["correo"],
            telefono=data.get("telefono"),
            tipo_usuario_param=data["tipo_usuario_param"],
            estatus=data.get("estatus", 1),
        )
        pwd_hash = make_password(new_password) if new_password else None
        self.repo.update(user_id, user, pwd_hash)

    def delete_user(self, user_id: int) -> None:
        self.repo.delete(user_id)
