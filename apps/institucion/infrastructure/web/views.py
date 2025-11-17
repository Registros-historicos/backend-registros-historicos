from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied

from .serializer import InstitucionSerializer, UpdateIdCepatSerializer, UpdateIdCoordinadortSerializer
from ...application.selectors.get_all_by_id_cepat import get_institutions_by_id_cepat
from ...application.selectors.update_id_cepat_by_id_institucion import update_institucion_id_cepat
from ...application.selectors.update_id_coor_by_institucion import update_institucion_id_coordinador


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_instituciones_con_cepat_view(request):
    """
    Vista para Listar todas las instituciones que coinciden con un 'id_cepat' (GET).
    """
    id_cepat_str = request.query_params.get('id_cepat')

    if not id_cepat_str:
        return Response(
            {"error": "El parámetro 'id_cepat' es requerido."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        id_cepat_int = int(id_cepat_str)
    except (ValueError, TypeError):
        return Response(
            {"error": "El 'id_cepat' debe ser un número entero."},
            status=status.HTTP_400_BAD_REQUEST
        )

    instituciones_list = get_institutions_by_id_cepat(id_cepat_int, request.user)

    serializer = InstitucionSerializer(instituciones_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_institucion_id_cepat_view(request, id_institucion: int):
    """
    Vista para Actualizar el id_cepat de una institución (PUT).
    """
    input_serializer = UpdateIdCepatSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)

    nuevo_id_cepat = input_serializer.validated_data.get('id_cepat')

    try:
        institucion_actualizada = update_institucion_id_cepat(
            id_institucion=id_institucion,
            id_cepat=nuevo_id_cepat,
            user=request.user
        )

        if not institucion_actualizada:
            return Response(
                {"detail": "Institución no encontrada o no se pudo actualizar."},
                status=status.HTTP_404_NOT_FOUND
            )

        output_serializer = InstitucionSerializer(institucion_actualizada)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    except PermissionDenied as e:
        return Response(
            {"detail": str(e)},
            status=status.HTTP_403_FORBIDDEN
        )
    except Exception as e:
        return Response(
            {"detail": f"Error al actualizar: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_institucion_id_coordinador_view(request, id_institucion: int):
    """
    Vista para Actualizar el id_cepat de una institución (PUT).
    """
    input_serializer = UpdateIdCoordinadortSerializer(data=request.data)
    input_serializer.is_valid(raise_exception=True)

    nuevo_id_coord = input_serializer.validated_data.get('id_coordinador')

    try:
        institucion_actualizada = update_institucion_id_coordinador(
            id_institucion=id_institucion,
            id_coordinador=nuevo_id_coord,
            user=request.user
        )

        if not institucion_actualizada:
            return Response(
                {"detail": "Institución no encontrada o no se pudo actualizar."},
                status=status.HTTP_404_NOT_FOUND
            )

        output_serializer = InstitucionSerializer(institucion_actualizada)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    except PermissionDenied as e:
        return Response(
            {"detail": str(e)},
            status=status.HTTP_403_FORBIDDEN
        )
    except Exception as e:
        return Response(
            {"detail": f"Error al actualizar: {e}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
