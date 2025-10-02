from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter

from apps.users.application.selectors.category_researchers import conteo_investigadores_por_categoria_selector
from apps.users.application.selectors.federal_entities_top10_queries import entidades_top10
from apps.users.infrastructure.repositories.user_repo import PgUserRepository
from apps.users.application.selectors.user_queries import UserQueriesSelector
from apps.users.application.services.user_comands import UserCommandsService
from apps.users.infrastructure.web.serializer import (
    UsuarioCreateSerializer,
    UsuarioUpdateSerializer,
    UsuarioResponseSerializer,
    EntidadTopSerializer
)
from rest_framework.permissions import AllowAny

class UsuarioViewSet(viewsets.ViewSet):
    
    permission_classes = [AllowAny] # permite acceso sin token / usar solo en app login / ESTE ES UN EJEMPLOOO
    """
    ViewSet para gestión de usuarios mediante funciones almacenadas en Postgres.
    
    Endpoints generados automáticamente por DRF Router:
    - **GET** `/api/usuarios/` — Listar usuarios, con filtros opcionales.
    - **POST** `/api/usuarios/` — Crear nuevo usuario.
    - **GET** `/api/usuarios/{id}/` — Obtener usuario por ID.
    - **PUT/PATCH** `/api/usuarios/{id}/` — Actualizar usuario.
    - **DELETE** `/api/usuarios/{id}/` — Eliminar usuario.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        repo = PgUserRepository()
        self.commands = UserCommandsService(repo)
        self.queries = UserQueriesSelector(repo)

    @extend_schema(
        summary="Listar usuarios",
        description="Obtiene la lista de usuarios con filtros opcionales por búsqueda y estatus.",
        parameters=[
            OpenApiParameter(name="q", description="Texto de búsqueda (nombre, apellidos, correo)", required=False, type=str),
            OpenApiParameter(name="estatus", description="Filtrar por estatus (1=activo, 0=inactivo)", required=False, type=int),
            OpenApiParameter(name="limit", description="Número máximo de resultados", required=False, type=int, default=50),
            OpenApiParameter(name="offset", description="Número de elementos a omitir (paginación)", required=False, type=int, default=0),
        ],
        responses={200: UsuarioResponseSerializer(many=True)},
    )
    def list(self, request):
        """Devuelve un listado de usuarios paginado y opcionalmente filtrado."""
        q = request.query_params.get("q", "")
        estatus = request.query_params.get("estatus")
        estatus = int(estatus) if estatus is not None else None
        limit = int(request.query_params.get("limit", 50))
        offset = int(request.query_params.get("offset", 0))

        items = self.queries.list(q=q, estatus=estatus, limit=limit, offset=offset)
        serializer = UsuarioResponseSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Obtener usuario por ID",
        responses={200: UsuarioResponseSerializer, 404: {"description": "Usuario no encontrado"}},
    )
    def retrieve(self, request, pk=None):
        """Obtiene un usuario específico por su ID."""
        item = self.queries.get(int(pk))
        if not item:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UsuarioResponseSerializer(item).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Crear usuario",
        request=UsuarioCreateSerializer,
        responses={201: UsuarioResponseSerializer},
    )
    def create(self, request):
        """Crea un nuevo usuario a partir de los datos proporcionados."""
        serializer = UsuarioCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data.copy()
        raw_pwd = payload.pop("password")
        new_id = self.commands.create_user(payload, raw_pwd)
        item = self.queries.get(new_id)
        return Response(UsuarioResponseSerializer(item).data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Actualizar usuario",
        request=UsuarioUpdateSerializer,
        responses={200: UsuarioResponseSerializer, 404: {"description": "Usuario no encontrado"}},
    )
    def update(self, request, pk=None):
        """Actualiza los datos de un usuario existente."""
        serializer = UsuarioUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data.copy()
        new_password = payload.pop("new_password", None)
        self.commands.update_user(int(pk), payload, new_password=new_password or None)
        item = self.queries.get(int(pk))
        if not item:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UsuarioResponseSerializer(item).data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Eliminar usuario",
        responses={204: {"description": "Usuario eliminado"}},
    )
    def destroy(self, request, pk=None):
        """Elimina un usuario por ID."""
        self.commands.delete_user(int(pk))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Usuario actual (dummy)",
        description="Endpoint de prueba para retornar info del usuario autenticado (por implementar).",
        responses={200: {"type": "object", "properties": {"ok": {"type": "boolean"}}}},
    )
    @action(detail=False, methods=["get"])
    def me(self, request):
        """Endpoint de ejemplo para representar el usuario autenticado."""
        return Response({"ok": True}, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Top 10 entidades federativas por número de registros",
        responses={200: EntidadTopSerializer(many=True)},
    )

    @action(detail=False, methods=["get"])
    def entidades_top10_view(self, request):
        resultado = entidades_top10()
        return Response(resultado, status=status.HTTP_200_OK)

    @extend_schema(
        summary="registros agrupados por tipo de investigador (Docente, Alumno, Administrativo)",
        responses={200: EntidadTopSerializer(many=True)},
    )
    @action(detail=False, methods=["get"])
    def categoria_investigadores_view(self, request):
        resultado = conteo_investigadores_por_categoria_selector()
        return Response(resultado, status=status.HTTP_200_OK)

