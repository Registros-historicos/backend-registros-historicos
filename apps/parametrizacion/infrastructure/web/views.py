from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .serializer import ParametrizacionSerializer
from apps.parametrizacion.application.selectors.parametrizacion_queries import (
    get_all_parametrizaciones, get_parametrizaciones_by_tema
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

    @extend_schema(summary="Obtener parametrizaciones por tema",
                   parameters=[{
                       "name": "id_tema",
                       "in": "query",
                       "schema": {"type": "integer", "example": 2}
                   }],
                   responses={200: ParametrizacionSerializer(many=True)})
    @action(detail=False, methods=["get"], url_path="by-tema")
    def by_tema(self, request):
        id_tema = request.query_params.get("id_tema")
        if not id_tema:
            return Response({"error": "Debe proporcionar id_tema"}, status=400)
        result = get_parametrizaciones_by_tema(int(id_tema))
        serializer = ParametrizacionSerializer(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
