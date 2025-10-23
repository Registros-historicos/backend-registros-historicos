from django.urls import path
from apps.users.infrastructure.web import views

urlpatterns = [
    # Ruta para /users/
    # GET: Listar todos
    # POST: Crear uno nuevo
    path(
        'users/',
        views.list_create_users_view,
        name='user-list-create'
    ),

    # Ruta para /users/usuario@ejemplo.com/
    # Usamos <path:correo> para capturar correctamente los emails
    # GET: Detalle de usuario
    # PUT: Actualizar usuario
    # DELETE: Deshabilitar usuario
    path(
        'users/<path:correo>/',
        views.user_detail_update_delete_view,
        name='user-detail-update-delete'
    ),
]