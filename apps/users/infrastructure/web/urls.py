from django.urls import path
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import (
    list_create_users_view,
    user_detail_update_delete_view,
    user_by_type_view,
    MeView, user_delate_by_id_view,
    user_profile_completo_view #agregado
)
from .auth_views import LoginView, RefreshView

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/refresh/", RefreshView.as_view(), name="auth-refresh"),

    # Ruta para /users/
    # GET: Listar todos
    # POST: Crear uno nuevo
    path(
        '',
        list_create_users_view,
        name='user-list-create'
    ),

    path(
        'tipo/<int:tipo>/',
        user_by_type_view,
        name='user-by-type'
    ),
    path(
        'delete/<int:id_user>/',
        user_delate_by_id_view,
        name='user_delate_by_id'
    ),

    # Ruta para /users/usuario@ejemplo.com/
    # Usamos <path:correo> para capturar correctamente los emails
    # GET: Detalle de usuario
    # PUT: Actualizar usuario
    # DELETE: Deshabilitar usuario
    path(
        '<path:correo>/',
        user_detail_update_delete_view,
        name='user-detail-update-delete'
    ),
    #AGREGADO
    # Nueva ruta para perfil completo
    path(
    'me/profile/',
    user_profile_completo_view,
    name='user-profile-completo'
),
]
