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
]
