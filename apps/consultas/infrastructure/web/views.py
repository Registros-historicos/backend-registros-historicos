from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.consultas.application.selectors.requests_by_type_queries import requests_impi, requests_indautor
from apps.consultas.application.selectors.category_researchers import conteo_investigadores_por_categoria_selector
from apps.consultas.application.selectors.federal_entities_top10_queries import entidades_top10
from apps.consultas.application.selectors.records_by_status import conteo_registros_por_estatus_selector
from apps.consultas.infrastructure.web.serializer import (
    EntidadTopSerializer,
    StatusCountSerializer,
    CategoriaInvestigadorSerializer,
    RequestTypeSerializer
)
from rest_framework.permissions import AllowAny

class ConsultaViewSet(viewsets.ViewSet):
    
    permission_classes = [AllowAny] # permite acceso sin token / usar solo en app login / ESTE ES UN EJEMPLOOO
    """
    ViewSet para tableros de consultas.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @extend_schema(
        summary="Top 10 entidades federativas por número de registros",
        responses={200: EntidadTopSerializer(many=True)},
    )

    @action(detail=False, methods=["get"])
    def entidades_top10_view(self, request):
        resultado = entidades_top10()
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Mostrar registros agrupados por estatus (Confirmada, Pendiente, Rechazada)",
        responses={200: EntidadTopSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def records_by_status_view(self, request):
        resultado = conteo_registros_por_estatus_selector()
        return Response(resultado, status=status.HTTP_200_OK)
        summary="registros agrupados por tipo de investigador (Docente, Alumno, Administrativo)",
        responses={200: EntidadTopSerializer(many=True)},
    
    @action(detail=False, methods=["get"])
    def categoria_investigadores_view(self, request):
        resultado = conteo_investigadores_por_categoria_selector()
        return Response(resultado, status=status.HTTP_200_OK)
        summary="registros agrupados por tipo de investigador (Docente, Alumno, Administrativo)",
        responses={200: CategoriaInvestigadorSerializer(many=True)},

    @extend_schema(
        summary="Requests grouped by type (IMPI)",
        responses={200: RequestTypeSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def requests_impi_view(self, request):
        result = requests_impi()
        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Requests grouped by type (INDAUTOR)",
        responses={200: RequestTypeSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def requests_indautor_view(self, request):
        result = requests_indautor()
        return Response(result, status=status.HTTP_200_OK)