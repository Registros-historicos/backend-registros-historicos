from django.urls import path
from .views import (
    list_create_users_view,
    user_detail_update_delete_view,
    user_by_type_view,
    MeView,
    user_delate_by_id_view,
    user_profile_completo_view,  # Import ya agregado
)
from .auth_views import LoginView, RefreshView

urlpatterns = [
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/refresh/", RefreshView.as_view(), name="auth-refresh"),

    # /api/usuarios/
    path(
        "",
        list_create_users_view,
        name="user-list-create",
    ),

    path(
        "tipo/<int:tipo>/",
        user_by_type_view,
        name="user-by-type",
    ),

    path(
        "delete/<int:id_user>/",
        user_delate_by_id_view,
        name="user_delate_by_id",
    ),

    # IMPORTANTE: poner esta ANTES de <path:correo>/
    path(
        "me/profile/",
        user_profile_completo_view,
        name="user-profile-completo",
    ),

    # /api/usuarios/<correo>/
    path(
        "<path:correo>/",
        user_detail_update_delete_view,
        name="user-detail-update-delete",
    ),
]
