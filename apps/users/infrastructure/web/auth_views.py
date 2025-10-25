from datetime import datetime, timezone
from django.conf import settings
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .auth_serializers import LoginResponseSerializer, LoginSerializer, RefreshRequestSerializer, RefreshResponseSerializer
from apps.users.application.services.auth_service import AuthService

class LoginView(APIView):
    permission_classes = [permissions.AllowAny] 

    def post(self, request):
        s = LoginSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        result = AuthService().login(s.validated_data["correo"], s.validated_data["password"])
        if not result:
            return Response({"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(LoginResponseSerializer(result).data, status=status.HTTP_200_OK)

class RefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        s = RefreshRequestSerializer(data=request.data)
        s.is_valid(raise_exception=True)
        token = s.validated_data["refresh"]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return Response({"detail":"refresh expirado"}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"detail":"refresh inválido"}, status=status.HTTP_401_UNAUTHORIZED)

        sub = str(payload.get("sub"))
        new_access, exp_access = AuthService()._issue({"sub": sub}, minutes=5)

        out = {"access": new_access, "access_exp": datetime.fromtimestamp(exp_access, tz=timezone.utc)}
        return Response(RefreshResponseSerializer(out).data, status=status.HTTP_200_OK)