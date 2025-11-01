# apps/investigadores/infrastructure/web/urls.py

from django.urls import path
from .views import InvestigadorViewSet

urlpatterns = [
    path('investigadores/create/', InvestigadorViewSet.as_view({'post': 'create_investigador'})),
    path('investigadores/update/', InvestigadorViewSet.as_view({'put': 'update_investigador'})),
    path('investigadores/delete/', InvestigadorViewSet.as_view({'delete': 'delete_investigador'})),
    path('investigadores/all/', InvestigadorViewSet.as_view({'get': 'all'})),
    path('investigadores/detail/', InvestigadorViewSet.as_view({'get': 'get_investigador_detail_view'})),
    path('adscripciones/create/', InvestigadorViewSet.as_view({'post': 'create_adscripcion'})),
    path('adscripciones/by-investigador/', InvestigadorViewSet.as_view({'get': 'get_adscripciones'})),
]
