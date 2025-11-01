from django.urls import path
from apps.registros.infrastructure.web.views import RegistroViewSet

urlpatterns = [
    path('', RegistroViewSet.as_view({
        'post': 'create',
        'get': 'list'
    }), name='registros'),

    path('search/', RegistroViewSet.as_view({
        'get': 'search'
    }), name='buscar_registros'),

    path('expediente/<str:no_expediente>/', RegistroViewSet.as_view({
        'get': 'by_expediente'
    }), name='registro_por_expediente'),

    path('<int:pk>/', RegistroViewSet.as_view({
        'get': 'retrieve',
        'put': 'update'
    }), name='detalle_registro'),

    path('<int:pk>/disable', RegistroViewSet.as_view({'patch': 'disable'}), name='estatus_deshabilitar'),
    path('<int:pk>/enable', RegistroViewSet.as_view({'patch': 'enable'}), name='estatus_habilitar'),

   path('indautor-bulk/', RegistroViewSet.as_view({'post': 'indautor_bulk'}), name='carga_masiva_indautor'),
    path('impi-bulk/', RegistroViewSet.as_view({'post': 'impi_bulk'}), name='carga_masiva_impi'),
]

