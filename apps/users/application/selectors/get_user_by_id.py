from ...domain.entities import Usuario
from django.core.exceptions import PermissionDenied
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.application.selectors.resolve_user_context import resolve_user_context

def get_user_profile_completo(user_id: int, current_user) -> dict | None:
    """
    Obtiene el perfil COMPLETO del usuario por ID incluyendo contexto
    """
    # Usar el repositorio existente en lugar de ORM directo
    repo = PgUserRepository()
    
    # Obtener usuario por ID (necesitarás agregar este método al repositorio)
    # O usar el método por correo que ya existe
    usuario = None
    
    # Si no, obtener primero el usuario actual para saber su correo
    current_user_id = getattr(current_user, "id", getattr(current_user, "sub", None))
    if not current_user_id or int(current_user_id) != user_id:
        raise PermissionDenied("No tienes permiso para acceder a este perfil")
    
    # Obtener usuario por correo del usuario actual
    user_email = getattr(current_user, "correo", None)
    if user_email:
        usuario = repo.get_by_correo_no_login(user_email)
    
    if not usuario:
        return None
    
    # Obtener contexto completo
    contexto = resolve_user_context(usuario.id_usuario)
    
    # Devolver perfil completo
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
            "ocupacion": contexto.get("rol_nombre") if contexto else "Usuario",
            "empresa": contexto.get("institucion_nombre") or contexto.get("cepat_nombre") or "TECNM",
            "direccion": {
                "ciudad": "No especificada",
                "estado": "No especificado",
                "direccion_linea": "Dirección no especificada",
                "codigo_postal": "00000"
            },
            "configuracion": {
                "idioma": "es",
                "zona_horaria": "America/Mexico_City",
                "email_habilitado": True,
                "sms_habilitado": True,
                "telefono_habilitado": False
            }
        }
    }