from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.consultas.application.selectors.requests_by_type_queries import requests_impi, requests_indautor
from apps.consultas.application.selectors.institutions_top10_queries import instituciones_top10
from apps.consultas.application.selectors.category_researchers import conteo_investigadores_por_categoria_selector
from apps.consultas.application.selectors.federal_entities_top10_queries import entidades_top10
from apps.consultas.application.selectors.records_by_status import conteo_registros_por_estatus_selector
from apps.consultas.application.selectors.economic_sectors_queries import conteo_registros_por_sector_selector
from apps.consultas.application.selectors.records_by_sex_queries import registros_por_sexo_selector
from apps.consultas.application.selectors.institutions_all_queries import instituciones_all
from apps.consultas.application.selectors.federal_entities_all_queries import entidades_all
from apps.consultas.application.selectors.sectors_activity_queries import sectores_actividad_top10
from apps.consultas.application.selectors.records_by_month_queries import registros_por_mes_selector
from apps.consultas.application.selectors.sectors_activity_all_selector import sectores_actividad_all
from apps.consultas.application.selectors.records_by_period import registros_por_periodo_selector
from apps.consultas.application.selectors.institutions_filtered_queries import instituciones_filtradas_selector
from apps.consultas.infrastructure.web.serializer import (
    EntidadTopSerializer,
    StatusCountSerializer,
    CategoriaInvestigadorSerializer,
    InstitucionTopSerializer,
    SectorEconomicoSerializer,
    RegistrosPorSexoSerializer,
    RequestTypeSerializer,
    SectorActividadSerializer,
    RegistrosPorMesSerializer,
    RegistrosPorPeriodoSerializer, InstitucionAllSerializer

)

from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.core.permissions import HasRole

class ConsultaViewSet(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated, HasRole]
    allowed_roles = [35] # Solo permite acceso al rol Administrador
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


    @extend_schema(
        summary="Conteo de registros por sexo de investigador",
        responses={200: RegistrosPorSexoSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def registros_por_sexo_view(self, request):
        resultado = registros_por_sexo_selector()
        return Response(resultado, status=status.HTTP_200_OK)
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

    @extend_schema(
        summary="Todas las instituciones con número de registros",
        responses={200: InstitucionAllSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def instituciones_all_view(self, request):
        resultado = instituciones_all()
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Todas las entidades federativas con número de registros",
        responses={200: EntidadTopSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def entidades_all_view(self, request):
        resultado = entidades_all()
        return Response(resultado, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Top 10 registros agrupados por sector/actividad económica",
        responses={200: SectorActividadSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def sectores_actividad_view(self, request):
        resultado = sectores_actividad_top10()
        return Response(resultado, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Todos los registros agrupados por sector/actividad económica",
        responses={200: SectorActividadSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def sectores_actividad_all_view(self, request):
        resultado = sectores_actividad_all()
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Conteo de registros por mes para un año específico",
        parameters=[
            OpenApiParameter(
                name='anio',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Año para filtrar los registros (ej: 2024)',
                required=True
            )
        ],
        responses={200: RegistrosPorMesSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def registros_por_mes_view(self, request):
        anio = request.query_params.get('anio')

        if not anio:
            return Response(
                {"error": "El parámetro 'anio' es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            anio = int(anio)
        except ValueError:
            return Response(
                {"error": "El parámetro 'anio' debe ser un número entero"},
                status=status.HTTP_400_BAD_REQUEST
            )

        resultado = registros_por_mes_selector(anio)
        return Response(resultado, status=status.HTTP_200_OK)
    
    
    @extend_schema(
        summary="Conteo de registros agrupados por año, mes y tipo de registro",
        parameters=[
            OpenApiParameter(
                name='inicio',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Fecha de inicio del rango (YYYY-MM-DD)',
                required=True
            ),
            OpenApiParameter(
                name='fin',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Fecha de fin del rango (YYYY-MM-DD)',
                required=True
            ),
            OpenApiParameter(
                name='fin',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Fecha de fin del rango (YYYY-MM-DD)',
                required=True
            )
        ],
        responses={200: RegistrosPorPeriodoSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def registros_por_periodo(self, request):
        """
        Endpoint para obtener registros agrupados por año, mes y tipo de registro
        dentro de un rango de fechas.
        """
        fecha_inicio = request.query_params.get('inicio')
        fecha_fin = request.query_params.get('fin')

        if not fecha_inicio or not fecha_fin:
            return Response(
                {"error": "Debe enviar los parámetros 'inicio' y 'fin' (YYYY-MM-DD)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            resultado = registros_por_periodo_selector(fecha_inicio, fecha_fin)
            serializer = RegistrosPorPeriodoSerializer(resultado, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    

    @extend_schema(
        summary="Instituciones filtradas por tipo (Federal/Descentralizado)",
        parameters=[
            OpenApiParameter(
                name='tipo_institucion',
                type=int,
                location=OpenApiParameter.QUERY,
                description='ID del tipo de institución (ej: 122=Descentralizado, 123=Federal)',
                required=True
            )
        ],
        responses={200: InstitucionTopSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def instituciones_filtradas_view(self, request):
        tipo_institucion = request.query_params.get('tipo_institucion')

        if not tipo_institucion:
            return Response(
                {"error": "El parámetro 'tipo_institucion' es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            tipo_institucion = int(tipo_institucion)
        except ValueError:
            return Response(
                {"error": "El parámetro 'tipo_institucion' debe ser un número entero"},
                status=status.HTTP_400_BAD_REQUEST
            )
        resultado = instituciones_filtradas_selector(tipo_institucion)
        return Response(resultado, status=status.HTTP_200_OK)
