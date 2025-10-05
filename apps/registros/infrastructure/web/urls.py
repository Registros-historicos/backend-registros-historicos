from django.urls import path
from apps.registros.infrastructure.web.views import RegistroViewSet

urlpatterns = [
    path('', RegistroViewSet.as_view({'post': 'create'}), name='crear_registro'),
    path('<int:pk>/', RegistroViewSet.as_view({'put': 'update'}), name='actualizar_registro'),
    path('<int:pk>/disable', RegistroViewSet.as_view({'patch': 'disable'}), name='estatus_deshabilitar'),
    path('<int:pk>/enable', RegistroViewSet.as_view({'patch': 'enable'}), name='estatus_habilitar'),
]
