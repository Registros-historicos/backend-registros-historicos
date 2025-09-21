# Aqui se colocaran mixins (clases reutilizables) comunes a todo el proyecto

from rest_framework.response import Response
from rest_framework import status


class ResponseMixin:
    """Mixin para estandarizar respuestas de API."""

    def success_response(self, data=None, message="OK", status_code=status.HTTP_200_OK):
        return Response({
            "status": "success",
            "message": message,
            "data": data
        }, status=status_code)

    def error_response(self, errors=None, message="Error", status_code=status.HTTP_400_BAD_REQUEST):
        return Response({
            "status": "error",
            "message": message,
            "errors": errors
        }, status=status_code)
