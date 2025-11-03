from datetime import datetime, timedelta, timezone
import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password

try:
    from apps.users.infrastructure.repositories.pg_utils import call_fn_rows  # type: ignore
except Exception:
    from apps.users.infrastructure.web.pg_utils import call_fn_rows  # type: ignore

class AuthService:

    def _issue(self, claims: dict, minutes: int = 200):
        now = datetime.now(timezone.utc)
        payload = {
            **claims,
            "iat": int(now.timestamp()),
            "exp": int((now + timedelta(minutes=minutes)).timestamp()),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return token, payload["exp"]

    def login(self, correo: str, raw_pwd: str):
        rows = call_fn_rows("f_busca_usuario_por_correo", [correo])
        if not rows: return None
        u = rows[0]
        pwd_stored = u.get("pwd") or u.get("pwd_hash") or u.get("password")
        if not pwd_stored or not check_password(raw_pwd, pwd_stored): return None

        # OBTENER CONTEXTO DEL USUARIO
        try:
            from apps.users.application.selectors.resolve_user_context import resolve_user_context
            contexto = resolve_user_context(u.get("id_usuario"))
        except Exception as e:
            print(f"⚠️ Error obteniendo contexto: {e}")
            contexto = None

        claims = {
            "sub": str(u.get("id_usuario")),    
            "correo": u.get("correo"),
            "tipo_usuario_param": u.get("tipo_usuario_param"),
            "estatus": u.get("estatus"),
            "nombre": u.get("nombre"),
        }
        access, exp_access = self._issue(claims, minutes=5)  
        refresh, exp_refresh = self._issue({"sub": claims["sub"]}, minutes=30)

        safe_user = {
            "id_usuario": u.get("id_usuario"),
            "correo": u.get("correo"),
            "tipo_usuario_param": u.get("tipo_usuario_param"),
            "estatus": u.get("estatus"),
            "nombre": u.get("nombre"),
        }
        
        return {
            "access": access,
            "access_exp": datetime.fromtimestamp(exp_access, tz=timezone.utc),
            "refresh": refresh,
            "refresh_exp": datetime.fromtimestamp(exp_refresh, tz=timezone.utc),
            "user": safe_user,
            # INCLUIR CONTEXTO EN LA RESPUESTA
            "contexto": contexto
        }