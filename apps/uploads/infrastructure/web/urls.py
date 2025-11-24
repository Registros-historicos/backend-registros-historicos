# apps/uploads/urls.py

from django.urls import path
from .views import PatentesUploadView, PatentesFileDetailView

urlpatterns = [
    path('patentes', PatentesUploadView.as_view(), name='patentes_upload'),
    path('patentes/<str:filename>', PatentesFileDetailView.as_view(), name='patentes_file_detail'),
]
