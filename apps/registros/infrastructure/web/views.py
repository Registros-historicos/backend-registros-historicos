from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import AllowAny
from .serializer import (
    RegistroSerializer,
    RegistroListSerializer,
    PaginatedRegistroSerializer,
)

from apps.registros.infrastructure.repositories.registros_repo import PostgresRegistroRepository
from apps.registros.application.services.registros_commands import RegistroService
from ...application.selectors.create_record import create_new_record
from ...application.selectors.disable_record import disable_record
from ...application.selectors.enable_record import enable_record
from ...application.selectors.update_record import update_records
from ...application.selectors.list_records import list_records
from ...application.selectors.search_records import search_records
from ...application.selectors.get_record_by_id import get_record_by_id
from ...application.selectors.get_record_by_expediente import get_record_by_expediente

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

    @extend_schema(
        summary="Listar registros por tipo (IMPI/INDAUTOR)",
        parameters=[
            OpenApiParameter(name="tipo", description="ID del tipo de registro (44=IMPI, 45=INDAUTOR)", required=True, type=int),
            OpenApiParameter(name="limit", description="Registros por página", required=False, type=int, default=10),
            OpenApiParameter(name="page", description="Número de página", required=False, type=int, default=1),
            OpenApiParameter(name="filter", description="Campo por el cual filtrar", required=False, type=str, default="fecha_solicitud"),
            OpenApiParameter(name="order", description="Orden de los resultados (asc/desc)", required=False, type=str, default="asc"),
        ],
        responses={200: PaginatedRegistroSerializer},
    )
    def list(self, request):
        """ Lista registros paginados por tipo """
        tipo = request.query_params.get("tipo")
        limit = int(request.query_params.get("limit", 10))
        page = int(request.query_params.get("page", 1))
        filter = request.query_params.get("filter", "id_registro")
        order = request.query_params.get("order", "desc")

        if not tipo:
            return Response(
                {"error": "El parámetro 'tipo' es obligatorio."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = list_records(int(tipo), page, limit, filter, order)
        return Response(result, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Buscar registros por texto",
        parameters=[
            OpenApiParameter(name="tipo", description="ID del tipo de registro", required=True, type=int),
            OpenApiParameter(name="q", description="Texto a buscar", required=True, type=str),
            OpenApiParameter(name="limit", description="Registros por página", required=False, type=int, default=10),
            OpenApiParameter(name="page", description="Número de página", required=False, type=int, default=1),
            OpenApiParameter(name="filter", description="Campo por el cual filtrar", required=False, type=str, default="id_registro "),
            OpenApiParameter(name="order", description="Orden de los resultados (asc/desc)", required=False, type=str, default="asc"),
       
        ],
        responses={200: PaginatedRegistroSerializer},
    )
    @action(detail=False, methods=["get"])
    def search(self, request):
        tipo = request.query_params.get("tipo")
        texto = request.query_params.get("q")
        limit = int(request.query_params.get("limit", 10))
        page = int(request.query_params.get("page", 1))
        filter = request.query_params.get("filter", "id_registro")
        order = request.query_params.get("order", "desc")

        if not tipo:
            return Response(
                {"error": "El parámetro 'tipo' es obligatorios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result = search_records(int(tipo), texto, page, limit, filter, order)
        return Response(result, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Obtener registro por ID",
        responses={200: RegistroListSerializer, 404: {"description": "No encontrado"}},
    )
    def retrieve(self, request, pk=None):
        registro = get_record_by_id(int(pk))
        if not registro:
            return Response(
                {"error": "Registro no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(registro, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Obtener registro por número de expediente",
        responses={200: RegistroListSerializer, 404: {"description": "No encontrado"}},
    )
    @action(detail=False, methods=["get"], url_path="expediente/(?P<no_expediente>[^/.]+)")
    def by_expediente(self, request, no_expediente=None):
        registro = get_record_by_expediente(no_expediente)
        if not registro:
            return Response(
                {"error": "Registro no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(registro, status=status.HTTP_200_OK)