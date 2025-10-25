<<<<<<< Updated upstream
from django.urls import path
from apps.users.infrastructure.web import views

urlpatterns = [
    # Ruta para /users/
    # GET: Listar todos
    # POST: Crear uno nuevo
    path(
        '',
        views.list_create_users_view,
        name='user-list-create'
    ),

    # Ruta para /users/usuario@ejemplo.com/
    # Usamos <path:correo> para capturar correctamente los emails
    # GET: Detalle de usuario
    # PUT: Actualizar usuario
    # DELETE: Deshabilitar usuario
    path(
        '<path:correo>/',
        views.user_detail_update_delete_view,
        name='user-detail-update-delete'
    ),
]
=======
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet
from .auth_views import LoginView, RefreshView

router = DefaultRouter()
router.register(r'', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/refresh/", RefreshView.as_view(), name="auth-refresh"),
    path("", include(router.urls)),
]
>>>>>>> Stashed changes
