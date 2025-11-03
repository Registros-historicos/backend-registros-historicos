from typing import Iterable, Optional, List
from apps.users.domain.entities import Usuario
from apps.users.domain.ports import UserRepositoryPort
from .pg_utils import call_fn_one, call_fn_rows, exec_fn_void
from django.db import connection


class PgUserRepository(UserRepositoryPort):

    def insertar(self, user: Usuario, pwd_hash: str) -> Optional[Usuario]:
        """
        Llama a la función de base de datos para insertar un usuario
        y devuelve la entidad Usuario completa.
        """
        rows = call_fn_rows(
            "public.f_inserta_usuario",
            [
                user.nombre,
                user.ape_pat,
                user.ape_mat,
                user.url_foto,
                user.correo,
                pwd_hash,
                user.telefono,
                user.tipo_usuario_param,
                user.estatus
            ]
        )

        if not rows:
            return None

        new_user_data = rows[0]

        if 'estatus_param' in new_user_data:
            new_user_data['estatus'] = new_user_data.pop('estatus_param')

        return Usuario(**new_user_data)

    def update(self, user: Usuario, pwd_hash: Optional[str] = None) -> Optional[Usuario]:
        """
        Llama a la función de base de datos para actualizar un usuario por su correo
        y devuelve la entidad Usuario actualizada.
        """
        rows = call_fn_rows(
            "public.f_actualiza_usuario_por_correo",
            [
                user.correo,
                user.nombre,
                user.ape_pat,
                user.ape_mat,
                user.url_foto,
                pwd_hash,
                user.telefono,
                user.tipo_usuario_param,
                user.estatus
            ]
        )

        if not rows:
            return None

        updated_user_data = rows[0]
        return Usuario(**updated_user_data)

    def deactivate_by_email(self, correo: str, inactive_status: int) -> Optional[Usuario]:
        """
        Deshabilita un usuario por su correo (borrado lógico).
        Llama a 'f_deshabilita_usuario' y devuelve el registro actualizado.

        Args:
            correo: El email del usuario a deshabilitar.
            inactive_status: El valor numérico para el estado "inactivo" (ej. 0).
        """
        rows = call_fn_rows(
            "public.f_deshabilita_usuario",
            [
                correo,
                inactive_status
            ]
        )

        if not rows:
            return None

        r = rows[0]

        if 'estatus_param' in r:
            r['estatus'] = r.pop('estatus_param')

        return Usuario(**r)

    def get_by_correo_no_login(self, correo: str) -> Optional[Usuario]:
        """
        Busca un usuario por su correo y devuelve el objeto Usuario.
        Esta función NO devuelve el hash de la contraseña.
        """
        rows = call_fn_rows(
            "public.f_busca_usuario_por_correo_no_login",
            [correo]
        )

        if not rows:
            return None

        r = rows[0]

        if 'estatus_param' in r:
            r['estatus'] = r.pop('estatus_param')

        return Usuario(**r)

    def get_all_usuers(self) -> List[Usuario]:
        """
        Devuelve una lista con todos los usuarios de la base de datos.
        """
        rows = call_fn_rows("public.f_buscar_todos_usuario", [])
        usuarios = []
        for r in rows:
            if 'estatus_param' in r:
                r['estatus'] = r.pop('estatus_param')

            usuarios.append(Usuario(**r))
        return usuarios

    def get_users_by_type(self, tipo: int) -> List[Usuario]:
        """
        Busca TODOS los usuarios por su tipo y devuelve una LISTA de objetos Usuario.
        """
        rows = call_fn_rows(
            "public.f_busca_usuario_por_tipo_usuario",
            [tipo]
        )
        usuarios = []
        for r in rows:
            if 'estatus_param' in r:
                r['estatus'] = r.pop('estatus_param')
            usuarios.append(Usuario(**r))

        return usuarios

    def delete_user_by_id(self, id_user: int) -> None:
        if not id_user:
            raise ValueError("El id del usuario no puede estar vacío o ser None")

        sql = f"SELECT public.f_elimina_usuario_by_id({id_user})"
        with connection.cursor() as cur:
            cur.execute(sql)
    #AGREGADO
    def get_by_id(self, user_id: int) -> Optional[Usuario]:
        """
        Busca un usuario por su ID
        """
        rows = call_fn_rows(
        "public.f_busca_usuario_por_id",
        [user_id]
        )
    
        if not rows:
            return None
    
        r = rows[0]
    
        if 'estatus_param' in r:
            r['estatus'] = r.pop('estatus_param')
    
        return Usuario(**r)
