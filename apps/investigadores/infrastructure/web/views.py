from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from apps.investigadores.infrastructure.web.serializers import (
    InvestigadorSerializer,
    AdscripcionSerializer,
)
from apps.investigadores.application.services.create_investigador import CreateInvestigadorService
from apps.investigadores.application.services.update_investigador import UpdateInvestigadorService
from apps.investigadores.application.services.delete_investigador import DeleteInvestigadorService
from apps.investigadores.application.services.create_adscripcion import CreateAdscripcionService
from apps.investigadores.application.selectors.get_investigadores import get_all_investigadores
from apps.investigadores.application.selectors.get_investigador_detail import get_investigador_detail
from apps.investigadores.application.selectors.get_adscripciones import get_adscripciones_by_investigador
from apps.investigadores.infrastructure.repositories.investigador_repository import InvestigadorRepository

repo = InvestigadorRepository()


class InvestigadorViewSet(viewsets.ViewSet):
    """
    ViewSet para gestionar Investigadores y sus Adscripciones.
    Usa funciones Postgres directamente (sin ORM).
    """

    permission_classes = [AllowAny]

    # === CREATE ===
    @extend_schema(
        summary="Crear un nuevo investigador",
        description="Crea un investigador usando la función f_crear_investigador de Postgres.",
        request=InvestigadorSerializer,
        responses={201: InvestigadorSerializer},
    )
    @action(detail=False, methods=["post"], url_path="create")
    def create_investigador(self, request):
        serializer = InvestigadorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = CreateInvestigadorService(repo)
        investigador = service.execute(**serializer.validated_data)
        return Response(
            InvestigadorSerializer(investigador).data, status=status.HTTP_201_CREATED
        )

    # === UPDATE ===
    @extend_schema(
        summary="Actualizar un investigador",
        description="Actualiza los datos de un investigador existente.",
        request=InvestigadorSerializer,
        parameters=[
            OpenApiParameter(
                name="id_investigador",
                description="ID del investigador a actualizar",
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={200: {"message": "Investigador actualizado"}},
    )
    @action(detail=False, methods=["put"], url_path="update")
    def update_investigador(self, request):
        id_investigador = request.query_params.get("id_investigador")
        if not id_investigador:
            return Response({"error": "Debe proporcionar id_investigador"}, status=400)

        try:
            id_investigador = int(id_investigador)
        except:
            return Response({"error": "id_investigador debe ser entero"}, status=400)

        serializer = InvestigadorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = UpdateInvestigadorService(repo)
        service.execute(id_investigador, **serializer.validated_data)
        return Response({"message": "Investigador actualizado correctamente"}, status=200)

    # === DELETE ===
    @extend_schema(
        summary="Eliminar un investigador",
        description="Elimina un investigador y sus adscripciones asociadas.",
        parameters=[
            OpenApiParameter(
                name="id_investigador",
                description="ID del investigador a eliminar",
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={200: {"message": "Investigador eliminado"}},
    )
    @action(detail=False, methods=["delete"], url_path="delete")
    def delete_investigador(self, request):
        id_investigador = request.query_params.get("id_investigador")
        if not id_investigador:
            return Response({"error": "Debe proporcionar id_investigador"}, status=400)

        try:
            id_investigador = int(id_investigador)
        except:
            return Response({"error": "id_investigador debe ser entero"}, status=400)

        service = DeleteInvestigadorService(repo)
        service.execute(id_investigador)
        return Response({"message": "Investigador eliminado correctamente"}, status=200)

    # === LIST ===
    @extend_schema(
        summary="Obtener todos los investigadores",
        responses={200: InvestigadorSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="all")
    def all(self, request):
        investigadores = get_all_investigadores()
        serializer = InvestigadorSerializer(investigadores, many=True)
        return Response(serializer.data, status=200)

    # === DETAIL (POR ID) ===
    @extend_schema(
        summary="Obtener detalle de un investigador",
        operation_id="investigador_detail_custom",  # FIX DE SWAGGER
        parameters=[
            OpenApiParameter(
                name="id_investigador",
                description="ID del investigador a consultar",
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={200: InvestigadorSerializer},
    )
    @action(detail=False, methods=["get"], url_path="detail")
    def get_investigador_detail_view(self, request):
        id_investigador = request.query_params.get("id_investigador")

        if not id_investigador:
            return Response({"error": "Debe proporcionar id_investigador"}, status=400)

        try:
            id_investigador = int(id_investigador)
        except:
            return Response({"error": "id_investigador debe ser entero"}, status=400)

        investigador = get_investigador_detail(id_investigador)

        if not investigador:
            return Response({"error": "No se encontró el investigador"}, status=404)

        return Response(InvestigadorSerializer(investigador).data, status=200)

    # === ADSCRIPCIONES ===
    @extend_schema(
        summary="Crear una adscripción para un investigador",
        description="Asocia un investigador con una institución mediante una adscripción.",
        request=AdscripcionSerializer,
        responses={201: AdscripcionSerializer},
    )
    @action(detail=False, methods=["post"], url_path="adscripcion/create")
    def create_adscripcion(self, request):
        serializer = AdscripcionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = CreateAdscripcionService(repo)
        adscripcion = service.execute(**serializer.validated_data)
        return Response(adscripcion, status=201)

    @extend_schema(
        summary="Obtener adscripciones por investigador",
        parameters=[
            OpenApiParameter(
                name="id_investigador",
                description="ID del investigador",
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={200: AdscripcionSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="adscripcion/by-investigador")
    def get_adscripciones(self, request):
        id_investigador = request.query_params.get("id_investigador")
        if not id_investigador:
            return Response({"error": "Debe proporcionar id_investigador"}, status=400)

        try:
            id_investigador = int(id_investigador)
        except ValueError:
            return Response({"error": "id_investigador debe ser un número entero"}, status=400)

        adscripciones = get_adscripciones_by_investigador(id_investigador)
        serializer = AdscripcionSerializer(adscripciones, many=True)
        return Response(serializer.data, status=200)
