from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet

router = DefaultRouter()
router.register(r'users', UsuarioViewSet, basename='usuario')


urlpatterns = [
    path('users/', include(router.urls)),
    path('tableros/entidades/top10/', UsuarioViewSet.as_view({'get': 'entidades_top10_view'}), name='entidades-top10'),
]
