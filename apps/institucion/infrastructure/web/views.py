from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated  # O la que uses
from rest_framework.response import Response
from rest_framework import status

from .serializer import InstitucionSerializer, UpdateIdCepatSerializer
from ...application.selectors.get_all_by_id_cepat import get_institutions_by_id_cepat
from ...application.selectors.update_id_cepat_by_id_institucion import update_institucion_id_cepat


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_instituciones_con_cepat_view(request):
    """
    Vista para Listar todas las instituciones que coinciden con un 'id_cepat' (GET).
    """
    if request.method == 'GET':

        # 1. Obtener el 'id_cepat' desde los query params de la URL
        id_cepat_str = request.query_params.get('id_cepat')

        # 2. Validar que el parámetro exista
        if not id_cepat_str:
            return Response(
                {"error": "El parámetro 'id_cepat' es requerido."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 3. Validar que sea un entero
            id_cepat_int = int(id_cepat_str)
        except (ValueError, TypeError):
            return Response(
                {"error": "El 'id_cepat' debe ser un número entero."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. Llamar al selector con el ID validado
        instituciones_list = get_institutions_by_id_cepat(id_cepat_int)

        # 5. Serializar los datos
        serializer = InstitucionSerializer(instituciones_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_institucion_id_cepat_view(request, id_institucion: int):
    """
    Vista para Actualizar el id_cepat de una institución (PUT).
    """
    if request.method == 'PUT':

        # 1. Validar datos de entrada (el body del request)
        input_serializer = UpdateIdCepatSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        nuevo_id_cepat = input_serializer.validated_data.get('id_cepat')

        # 2. Llamar al comando
        try:
            institucion_actualizada = update_institucion_id_cepat(
                id_institucion=id_institucion,
                id_cepat=nuevo_id_cepat
            )
        except Exception as e:
            # Manejo de errores (ej. si la función de DB falla)
            return Response(
                {"detail": f"Error al actualizar: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # 3. Serializar y responder
        if not institucion_actualizada:
            return Response(
                {"detail": "Institución no encontrada o no se pudo actualizar."},
                status=status.HTTP_404_NOT_FOUND
            )

        output_serializer = InstitucionSerializer(institucion_actualizada)
        return Response(output_serializer.data, status=status.HTTP_200_OK)
