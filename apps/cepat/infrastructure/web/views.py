from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied

# Selectors (Queries) - SÓLO PARA GET
from ...application.selectors.cepat_queries import get_all_cepat, get_cepat_by_id

# Services (Commands) - PARA POST, PUT, DELETE
from ...application.services.cepat_commands import CepatCommandsService
from ...infrastructure.repositories.pg_utils import PgCepatRepository

# Serializers
from .serializer import CepatSerializer, CepatInputSerializer, CepatPatchUsuarioSerializer, CepatPatchResultSerializer


@api_view(['GET', 'POST'])
def list_create_view(request):
    """
    Vista para Listar (GET) o Crear (POST).
    """
    if request.method == 'GET':
        # --- LECTURA ---
        cepats = get_all_cepat(request.user)
        serializer = CepatSerializer(cepats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # --- ESCRITURA ---
        input_serializer = CepatInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        repo = PgCepatRepository()
        service = CepatCommandsService(repo)

        try:
            nombre = input_serializer.validated_data['nombre']
            id_usuario = input_serializer.validated_data['id_usuario']

            new_cepat = service.create_cepat(
                request.user,
                nombre,
                id_usuario
            )

            output_serializer = CepatSerializer(new_cepat)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": f"Error al crear: {str(e)}"}, status=status.HTTP_409_CONFLICT)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def detail_update_delete_view(request, cepat_id: int):
    """
    Vista para Obtener (GET), Actualizar (PUT) o Eliminar (DELETE).
    """

    # --- LECTURA (GET) ---
    if request.method == 'GET':
        cepat = get_cepat_by_id(cepat_id, request.user)
        if not cepat:
            return Response({"error": "Cepat no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CepatSerializer(cepat)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # --- ESCRITURA (PUT) ---
    elif request.method == 'PUT':
        input_serializer = CepatInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        repo = PgCepatRepository()
        service = CepatCommandsService(repo)

        try:
            nombre = input_serializer.validated_data['nombre']
            id_usuario = input_serializer.validated_data['id_usuario']

            updated_cepat = service.update_cepat(
                request.user,
                cepat_id,
                nombre,
                id_usuario
            )

            if not updated_cepat:
                return Response({"error": "Cepat no encontrado para actualizar"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CepatSerializer(updated_cepat)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": f"Error al actualizar: {str(e)}"}, status=status.HTTP_409_CONFLICT)

    elif request.method == 'PATCH':
        input_serializer = CepatPatchUsuarioSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        repo = PgCepatRepository()
        service = CepatCommandsService(repo)

        try:
            id_usuario = input_serializer.validated_data['id_usuario']

            updated_cepat_result = service.update_cepat_usuario(
                request.user,
                cepat_id,
                id_usuario
            )

            if not updated_cepat_result:
                return Response({"error": "Cepat no encontrado para actualizar"}, status=status.HTTP_404_NOT_FOUND)

            serializer = CepatPatchResultSerializer(updated_cepat_result)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": f"Error al actualizar: {str(e)}"}, status=status.HTTP_409_CONFLICT)

    elif request.method == 'DELETE':

        cepat_existente = get_cepat_by_id(cepat_id, request.user)
        if not cepat_existente:
            return Response({"error": "Cepat no encontrado para eliminar"}, status=status.HTTP_404_NOT_FOUND)

        repo = PgCepatRepository()
        service = CepatCommandsService(repo)

        try:
            service.delete_cepat(request.user, cepat_id)

            return Response(status=status.HTTP_204_NO_CONTENT)

        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": f"Error al eliminar: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)