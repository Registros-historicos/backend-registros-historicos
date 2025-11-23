from django.core.exceptions import PermissionDenied
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.application.selectors.resolve_user_context import resolve_user_context


def get_user_profile_completo(user_id: int, current_user) -> dict | None:
    """
    Obtiene el perfil COMPLETO del usuario por ID incluyendo contexto.

    Para evitar errores con funciones de BD que todavía no existan,
    se usa el correo del usuario autenticado (igual que en login),
    y de ahí se obtiene id_usuario e institución.
    """
    repo = PgUserRepository()

    # Validar que el usuario autenticado solo consulte su propio perfil
    current_id = (
        getattr(current_user, "id_usuario", None)
        or getattr(current_user, "id", None)
        or getattr(current_user, "sub", None)
    )
    if not current_id:
        raise PermissionDenied("Usuario no autenticado")

    if int(current_id) != int(user_id):
        raise PermissionDenied("No tienes permiso para acceder a este perfil")

    # Obtener correo del usuario autenticado (igual que en login)
    correo = getattr(current_user, "correo", None) or getattr(current_user, "email", None)
    if not correo:
        # Si no hay correo, no podemos buscar al usuario en BD
        return None

    # Usar función que ya existe y funciona en tu repo
    usuario = repo.get_by_correo_no_login(correo)
    if not usuario:
        return None

    # Resolver contexto (institución, CEPAT, rol, etc.)
    contexto = resolve_user_context(usuario.id_usuario) if usuario.id_usuario else None

    # Armar perfil completo
    return {
        "id_usuario": usuario.id_usuario,
        "nombre": usuario.nombre,
        "ape_pat": usuario.ape_pat,
        "ape_mat": usuario.ape_mat,
        "correo": usuario.correo,
        "telefono": usuario.telefono,
        "url_foto": usuario.url_foto,
        "tipo_usuario_param": usuario.tipo_usuario_param,
        "estatus": usuario.estatus,
        "contexto": contexto,
        "perfil": {
            "nombre_completo": f"{usuario.nombre} {usuario.ape_pat} {usuario.ape_mat}".strip(),
            "ocupacion": (contexto or {}).get("rol_nombre") if contexto else "Usuario",
            # Aquí sale la institución/CEPAT ligada al id_usuario
            "empresa": (
                (contexto or {}).get("institucion_nombre")
                or (contexto or {}).get("cepat_nombre")
                or "TECNM"
            ),
            "direccion": {
                "ciudad": "No especificada",
                "estado": "No especificado",
                "direccion_linea": "Dirección no especificada",
                "codigo_postal": "00000",
            },
            "configuracion": {
                "idioma": "es",
                "zona_horaria": "America/Mexico_City",
                "email_habilitado": True,
                "sms_habilitado": True,
                "telefono_habilitado": False,
            },
        },
    }
