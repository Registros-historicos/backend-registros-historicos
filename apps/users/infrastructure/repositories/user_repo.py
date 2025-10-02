from typing import Iterable, Optional
from apps.users.domain.entities import Usuario
from apps.users.domain.ports import UserRepositoryPort
from .pg_utils import call_fn_one, call_fn_rows, exec_fn_void

class PgUserRepository(UserRepositoryPort):

    def create(self, user: Usuario, pwd_hash: str) -> int:
        new_id = call_fn_one(
            "public.fn_usuario_create",
            [
                user.nombre, user.ape_pat, user.ape_mat, user.url_foto,
                user.correo, pwd_hash, user.telefono,
                user.tipo_usuario_param, user.estatus
            ]
        )
        return int(new_id)

    def update(self, user_id: int, user: Usuario, pwd_hash: Optional[str] = None) -> None:
        exec_fn_void(
            "public.fn_usuario_update",
            [
                user_id, user.nombre, user.ape_pat, user.ape_mat, user.url_foto,
                user.correo, pwd_hash, user.telefono, user.tipo_usuario_param, user.estatus
            ]
        )

    def delete(self, user_id: int) -> None:
        exec_fn_void("public.fn_usuario_delete", [user_id])

    def get_by_id(self, user_id: int) -> Optional[Usuario]:
        rows = call_fn_rows("public.fn_usuario_get_by_id", [user_id])
        if not rows:
            return None
        r = rows[0]
        return Usuario(**r)

    def list(self, q: str = "", estatus: Optional[int] = None,
             limit: int = 50, offset: int = 0) -> Iterable[Usuario]:
        rows = call_fn_rows("public.fn_usuario_list", [q, estatus, limit, offset])
        return [Usuario(**r) for r in rows]
