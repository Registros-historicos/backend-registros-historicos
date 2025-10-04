from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.consultas.application.selectors.institutions_top10_queries import instituciones_top10
from apps.consultas.application.selectors.category_researchers import conteo_investigadores_por_categoria_selector
from apps.consultas.application.selectors.federal_entities_top10_queries import entidades_top10
from apps.consultas.application.selectors.records_by_status import conteo_registros_por_estatus_selector
from apps.consultas.application.selectors.economic_sectors_queries import conteo_registros_por_sector_selector
from apps.consultas.infrastructure.web.serializer import (
    EntidadTopSerializer,
    StatusCountSerializer,
    CategoriaInvestigadorSerializer,
    InstitucionTopSerializer,
    SectorEconomicoSerializer,
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
        summary="Top 10 instituciones por número de registros",
        responses={200: InstitucionTopSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def instituciones_top10_view(self, request):
        resultado = instituciones_top10()
        return Response(resultado, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Registros agrupados por sector económico",
        responses={200: SectorEconomicoSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def registros_por_sector_view(self, request):
        resultado = conteo_registros_por_sector_selector()
        return Response(resultado, status=status.HTTP_200_OK)