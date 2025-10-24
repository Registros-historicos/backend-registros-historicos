from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Selectors (Queries) - SÓLO PARA GET
from ...application.selectors.cepat_queries import get_all_cepat, get_cepat_by_id

# Services (Commands) - PARA POST, PUT, DELETE
from ...application.services.cepat_commands import CepatCommandsService
from ...infrastructure.repositories.pg_utils import PgCepatRepository

# Serializers
from .serializer import CepatSerializer, CepatInputSerializer


@api_view(['GET', 'POST'])
def list_create_view(request):
    """
    Vista para Listar (GET) o Crear (POST).
    """
    if request.method == 'GET':
        # --- LECTURA ---
        # 1. Llama al SELECTOR
        cepats = get_all_cepat()
        serializer = CepatSerializer(cepats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # --- ESCRITURA ---
        input_serializer = CepatInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 1. Llama al SERVICIO
        repo = PgCepatRepository()
        service = CepatCommandsService(repo)

        try:
            nombre = input_serializer.validated_data['nombre']
            new_cepat = service.create_cepat(nombre)  # <-- USA EL SERVICIO

            output_serializer = CepatSerializer(new_cepat)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"Error al crear: {str(e)}"}, status=status.HTTP_409_CONFLICT)


@api_view(['GET', 'PUT', 'DELETE'])
def detail_update_delete_view(request, cepat_id: int):
    """
    Vista para Obtener (GET), Actualizar (PUT) o Eliminar (DELETE).
    """

    if request.method == 'GET':
        # --- LECTURA ---
        # 1. Llama al SELECTOR
        cepat = get_cepat_by_id(cepat_id)
        if not cepat:
            return Response({"error": "Cepat no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CepatSerializer(cepat)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        # --- ESCRITURA ---
        input_serializer = CepatInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 1. Llama al SERVICIO
        repo = PgCepatRepository()
        service = CepatCommandsService(repo)

        nombre = input_serializer.validated_data['nombre']
        updated_cepat = service.update_cepat(cepat_id, nombre)  # <-- USA EL SERVICIO

        if not updated_cepat:
            return Response({"error": "Cepat no encontrado para actualizar"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CepatSerializer(updated_cepat)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # --- ESCRITURA ---
        # 1. Llama al SERVICIO
        repo = PgCepatRepository()
        service = CepatCommandsService(repo)

        deleted_cepat = service.delete_cepat(cepat_id)  # <-- USA EL SERVICIO

        if not deleted_cepat:
            return Response({"error": "Cepat no encontrado para eliminar"}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


from django.shortcuts import render

# Create your views here.
