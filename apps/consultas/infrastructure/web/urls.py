from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultaViewSet

router = DefaultRouter()
router.register(r'tableros', ConsultaViewSet, basename='tableros')


urlpatterns = [
    path('entidades/top10/', ConsultaViewSet.as_view({'get': 'entidades_top10_view'}), name='entidades-top10'),
    path('registros/estatus/', ConsultaViewSet.as_view({'get': 'records_by_status_view'}), name='registros-por-estatus'),
    path('investigadores/categorias/', ConsultaViewSet.as_view({'get': 'categoria_investigadores_view'}), name='categoria-investigadores'),
    path('instituciones/top10/', ConsultaViewSet.as_view({'get': 'instituciones_top10_view'}), name='instituciones-top10'),
    path('sectores/', ConsultaViewSet.as_view({'get': 'registros_por_sector_view'}), name='registros-por-sector'),
    path('investigadores/sexo/', ConsultaViewSet.as_view({'get': 'registros_por_sexo_view'}), name='registros-por-sexo'),
    path('solicitudes/impi/', ConsultaViewSet.as_view({'get': 'requests_impi_view'}), name='requests-impi'),
    path('solicitudes/indautor/', ConsultaViewSet.as_view({'get': 'requests_indautor_view'}), name='requests-indautor'),
    path('instituciones/all/', ConsultaViewSet.as_view({'get': 'instituciones_all_view'}), name='instituciones-all'),
    path('entidades/all/', ConsultaViewSet.as_view({'get': 'entidades_all_view'}), name='entidades-all'),
    path('sectores/actividad/', ConsultaViewSet.as_view({'get': 'sectores_actividad_view'}), name='sectores-actividad'),
    path('registros/mes/', ConsultaViewSet.as_view({'get': 'registros_por_mes_view'}), name='registros-por-mes'),
    path('registros/periodo/', ConsultaViewSet.as_view({'get': 'registros_por_periodo'}), name='registros-por-periodo'),
    path('sectores/actividad/all/', ConsultaViewSet.as_view({'get': 'sectores_actividad_all_view'}), name='sectores-actividad-all'),
    path('instituciones/filtradas/', ConsultaViewSet.as_view({'get': 'instituciones_filtradas_view'}), name='instituciones-filtradas'),
    path('investigadores/por-coordinador/', ConsultaViewSet.as_view({'get': 'investigadores_por_coordinador_view'}), name='investigadores-por-coordinador'),
    path('usuarios/por-estados-cepat/', ConsultaViewSet.as_view({'get': 'usuarios_por_estados_cepat_view'}), name='usuarios-por-estados-cepat'),
    path('programas-educativos/', ConsultaViewSet.as_view({'get': 'programas_educativos_view'}), name='programas-educativos'),
    path('registros/por-programa/', ConsultaViewSet.as_view({'get': 'registros_por_programa_view'}), name='registros-por-programa'),
]
