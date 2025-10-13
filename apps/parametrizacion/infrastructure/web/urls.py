from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParametrizacionViewSet

router = DefaultRouter()
router.register(r'', ParametrizacionViewSet, basename='parametrizaciones')



urlpatterns = [
    path("", include(router.urls)),
]
