from django.urls import path
from . import views

urlpatterns = [
    # Ruta para /api/cepat/
    # GET: Listar todos
    # POST: Crear uno nuevo
    path(
        '',
        views.list_create_view,
        name='cepat-list-create'
    ),

    # Ruta para /api/cepat/<id>/
    # GET: Detalle
    # PUT: Actualizar
    # DELETE: Eliminar
    path(
        '<int:cepat_id>/',
        views.detail_update_delete_view,
        name='cepat-detail-update-delete'
    ),
]

