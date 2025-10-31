from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes, OpenApiExample

from .serializer import ParametrizacionSerializer, EstadoSerializer, InstitucionPorEstadoSerializer
from apps.parametrizacion.application.selectors.parametrizacion_queries import (
    get_all_parametrizaciones, get_parametrizaciones_by_tema, get_estado_param, get_instituciones_por_estado,
    get_estados_by_id_user
)

from rest_framework.permissions import AllowAny

class ParametrizacionViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]  # permite acceso sin token / usar solo en app login / ESTE ES UN EJEMPLOOO

    @extend_schema(summary="Obtener todas las parametrizaciones",
                   responses={200: ParametrizacionSerializer(many=True)})
    @action(detail=False, methods=["get"], url_path="all")
    def all(self, request):
        result = get_all_parametrizaciones()
        serializer = ParametrizacionSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    @extend_schema(
        summary="Obtener parametrizaciones por tema",
        description="Devuelve todas las parametrizaciones asociadas a un tema específico.",
        parameters=[
            OpenApiParameter(
                name="id_tema",
                description="ID del tema a consultar",
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                
            ),
        ],
        responses={200: ParametrizacionSerializer(many=True)},
    )
    @action(detail=False, methods=["get"], url_path="by-tema")
    def by_tema(self, request):
        id_tema = request.query_params.get("id_tema")
        if not id_tema:
            return Response({"error": "Debe proporcionar id_tema"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            id_tema = int(id_tema)
        except ValueError:
            return Response({"error": "id_tema debe ser un número entero"}, status=status.HTTP_400_BAD_REQUEST)
        result = get_parametrizaciones_by_tema(id_tema)
        serializer = ParametrizacionSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="estados")
    def estados(self, request):
        result = get_estado_param()
        serializer = EstadoSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Obtener instituciones por entidad federativa",
        description="Devuelve todas las instituciones asociadas a una entidad federativa específica.",
        responses={200: InstitucionPorEstadoSerializer(many=True)},
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="instituciones/estado/(?P<id_entidad_federativa>[^/.]+)"
    )
    def instituciones_por_estado(self, request, id_entidad_federativa=None):
        try:
            id_entidad_federativa = int(id_entidad_federativa)
        except (TypeError, ValueError):
            return Response({"error": "id_entidad_federativa debe ser un número entero"},
                            status=status.HTTP_400_BAD_REQUEST)

        result = get_instituciones_por_estado(id_entidad_federativa)
        serializer = InstitucionPorEstadoSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        url_path="estados/(?P<id_usuario>[^/.]+)"
    )
    def estados_by_id_user(self, request, id_usuario=None):
        try:
            id_user = int(id_usuario)
        except (TypeError, ValueError):
            return Response({"error": "id_entidad_federativa debe ser un número entero"},
                            status=status.HTTP_400_BAD_REQUEST)
        result = get_estados_by_id_user(id_user)
        serializer = EstadoSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

