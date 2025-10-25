from rest_framework.permissions import BasePermission

class HasRole(BasePermission):
    
    def has_permission(self, request, view):
        allowed = getattr(view, "allowed_roles", None)
        if not allowed:
            return True
        try:
            return int(getattr(request.user, "tipo_usuario_param", -1)) in set(int(x) for x in allowed)
        except Exception:
            return False
