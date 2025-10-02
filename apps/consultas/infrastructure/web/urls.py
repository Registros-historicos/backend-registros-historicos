from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConsultaViewSet

router = DefaultRouter()
router.register(r'consultas', ConsultaViewSet, basename='consultas')

app_name = 'consultas'

urlpatterns = [
    path('tableros/entidades/top10/', ConsultaViewSet.as_view({'get': 'entidades_top10_view'}), name='entidades-top10'),
    path('tableros/registros/estatus/', ConsultaViewSet.as_view({'get': 'records_by_status_view'}), name='registros-por-estatus'),
    path('tableros/investigadores/categorias/', ConsultaViewSet.as_view({'get': 'categoria_investigadores_view'}), name='categoria-investigadores'),

    
    path("", include(router.urls)),
]
