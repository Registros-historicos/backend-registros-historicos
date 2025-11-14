from django.urls import path
from .views import (
    list_instituciones_con_cepat_view,
    update_institucion_id_cepat_view, update_institucion_id_coordinador_view
)

urlpatterns = [
    # GET /api/institucion/con-cepat/
    path(
        'con-cepat/',
        list_instituciones_con_cepat_view,
        name='institucion-list-con-cepat'
    ),

    # PUT /api/institucion/123/actualizar-id-cepat/
    path(
        '<int:id_institucion>/actualizar-id-cepat/',
        update_institucion_id_cepat_view,
        name='institucion-update-id-cepat'
    ),

    path(
        'usuario/<int:id_institucion>/',
        update_institucion_id_coordinador_view,
        name='institucion-update-id-coordinador'
    ),
]