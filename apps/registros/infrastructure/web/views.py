from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from .serializer import RegistroSerializer

from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository
from apps.registros.application.services.registros_commands import RegistroService
from ...application.selectors.create_record import create_new_record
from ...application.selectors.disable_record import disable_record
from ...application.selectors.enable_record import enable_record
from ...application.selectors.update_record import update_records

service = RegistroService(PostgresRegistroRepository())

class RegistroViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    permission_classes = [AllowAny]  # permite acceso sin token / usar solo en app login / ESTE ES UN EJEMPLOOO
    """
    ViewSet para tableros de consultas.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @extend_schema(
        summary="Crear registro",
        responses={200: RegistroSerializer},
    )
    def create(self, request):
        serializer = RegistroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = create_new_record(serializer.validated_data)
        return Response(result, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Actualizar registro",
        request=RegistroSerializer,
        responses={200: RegistroSerializer},
    )
    def update(self, request, pk=None):
        serializer = RegistroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        registro = update_records(pk, serializer.validated_data)
        return Response(RegistroSerializer(registro).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Deshabilitar registro",
        responses={200: RegistroSerializer},
    )
    @action(detail=True, methods=["patch"])
    def disable(self, request, pk=None):
        disable_record(pk)
        return Response({"id_registro": pk, "habilitado": False}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Habilitar registro",
        responses={200: RegistroSerializer},
    )
    @action(detail=True, methods=["patch"])
    def enable(self, request, pk=None):
        enable_record(pk)
        return Response({"id_registro": pk, "habilitado": True}, status=status.HTTP_200_OK)
