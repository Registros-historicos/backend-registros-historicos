from typing import Iterable, Optional, List
from apps.users.domain.entities import Usuario
from apps.users.domain.ports import UserRepositoryPort
from .pg_utils import call_fn_one, call_fn_rows, exec_fn_void

class PgUserRepository(UserRepositoryPort):

    def insertar(self, user: Usuario, pwd_hash: str) -> Optional[Usuario]:
        """
        Llama a la función de base de datos para insertar un usuario
        y devuelve la entidad Usuario completa.
        """
        rows = call_fn_rows(
            "public.f_inserta_usuario_test", # O f_inserta_usuario si usas esa
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

    def update(self, user_id: int, user: Usuario, pwd_hash: Optional[str] = None) -> None:
        exec_fn_void(
            "public.f_actualiza_usuario_por_correo",  # <-- Nombre de la función actualizado
            [
                # --- Parámetros reordenados ---
                user.correo,  # p_correo (ahora es el identificador)
                user.nombre,  # p_nombre
                user.ape_pat,  # p_ape_pat
                user.ape_mat,  # p_ape_mat
                user.url_foto,  # p_url_foto
                pwd_hash,  # p_pwd
                user.telefono,  # p_telefono
                user.tipo_usuario_param,  # p_tipo_usuario_param
                user.estatus  # p_estatus_param
                # El user_id ya no se pasa, la nueva función no lo usa
            ]
        )

    def deactivate_by_email(self, correo: str, inactive_status: int) -> Optional[Usuario]:
        """
        Deshabilita un usuario por su correo (borrado lógico).
        Llama a 'f_deshabilita_usuario' y devuelve el registro actualizado.

        Args:
            correo: El email del usuario a deshabilitar.
            inactive_status: El valor numérico para el estado "inactivo" (ej. 0).
        """
        rows = call_fn_rows(
            "public.f_deshabilita_usuario",  # <-- Nombre de la función SQL actualizado
            [
                correo,  # p_correo
                inactive_status  # p_estatus_inactivo
            ]
        )

        if not rows:
            return None

        r = rows[0]

        # Renombrar 'estatus_param' para que coincida con tu clase Usuario
        if 'estatus_param' in r:
            r['estatus'] = r.pop('estatus_param')

        return Usuario(**r)

    def get_by_correo_no_login(self, correo: str) -> Optional[Usuario]:
        """
        Busca un usuario por su correo y devuelve el objeto Usuario.
        Esta función NO devuelve el hash de la contraseña.
        """
        rows = call_fn_rows(
            "public.f_busca_usuario_por_correo_no_login",  # <-- Llama a la nueva función
            [correo]
        )

        if not rows:
            return None

        r = rows[0]

        # --- Adaptar el diccionario ---
        # 1. Renombrar 'estatus_param' para que coincida con tu clase Usuario
        if 'estatus_param' in r:
            r['estatus'] = r.pop('estatus_param')

        # 2. Ya no es necesario eliminar 'pwd', la nueva SP no lo devuelve.
        # --- Fin de la adaptación ---

        return Usuario(**r)

    def get_all_usuers(self) -> List[Usuario]:
        """
        Devuelve una lista con todos los usuarios de la base de datos.
        """
        rows = call_fn_rows("public.f_buscar_todos_usuario", [])  # <-- Llama a la función SQL renombrada

        usuarios = []
        for r in rows:
            # Renombrar 'estatus_param' para que coincida con tu clase Usuario
            if 'estatus_param' in r:
                r['estatus'] = r.pop('estatus_param')

            usuarios.append(Usuario(**r))

        return usuarios
