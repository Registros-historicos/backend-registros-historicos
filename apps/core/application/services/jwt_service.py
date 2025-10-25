import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions

class JWTUser:
    def __init__(self, **claims):
        for k, v in claims.items():
            setattr(self, k, v)
        if not hasattr(self, "id") and hasattr(self, "sub"):
            setattr(self, "id", self.sub)

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

class JWTAuth(BaseAuthentication):
    keyword = b"Bearer"

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower():
            return None

        if len(auth) != 2:
            raise exceptions.AuthenticationFailed("Cabecera Authorization inválida")

        token = auth[1]
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
                options={"require": ["exp", "iat"]},
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expirado")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Token inválido")

        user = JWTUser(**payload)
        return (user, None)
