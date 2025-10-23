from sqlite3 import IntegrityError

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Importar Selectores (Casos de Uso)
from apps.users.application.selectors.get_all_users import get_all_users
from apps.users.application.selectors.get_user_by_email import list_users
from apps.users.application.selectors.create_user import create_new_user
from apps.users.application.selectors.update_user_by_email import update_user
from apps.users.application.selectors.deactivate_user_by_email import deactivate_user_by_email

# Importar Serializers
from .serializer import UsuarioSerializer, UserCreateSerializer
from ...domain.entities import Usuario


@api_view(['GET', 'POST'])
def list_create_users_view(request):
    """
    Vista para Listar todos los usuarios (GET) o Crear uno nuevo (POST).
    """
    if request.method == 'GET':
        # 1. Llamar al selector para obtener todos los usuarios
        usuarios_list = get_all_users()

        # 2. Serializar los datos
        serializer = UsuarioSerializer(usuarios_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    elif request.method == 'POST':

        serializer = UserCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        raw_password = data.pop('password')

        try:

            user_entity = Usuario(

                id_usuario=None,

                nombre=data['nombre'],

                ape_pat=data['ape_pat'],

                ape_mat=data.get('ape_mat'),

                url_foto=data.get('url_foto'),

                correo=data['correo'],

                telefono=data.get('telefono'),

                tipo_usuario_param=data['tipo_usuario_param'],

                estatus=data['estatus']

            )

            # --- CAMBIO CLAVE 1: Llama al selector correcto ---

            new_user_obj = create_new_user(user_entity, raw_password)

            if not new_user_obj:
                return Response({"error": "No se pudo crear el usuario."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # --- CAMBIO CLAVE 2: Serializa el objeto devuelto por la BD ---

            response_serializer = UsuarioSerializer(new_user_obj)

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)


        # --- CAMBIO CLAVE 3: Manejo de error específico ---

        except IntegrityError:

            return Response({"error": f"El correo '{data['correo']}' ya existe."}, status=status.HTTP_409_CONFLICT)

        except Exception as e:

            return Response({"error": f"Error inesperado al crear usuario: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_update_delete_view(request, correo: str):
    """
    Vista para Obtener (GET), Actualizar (PUT) o Deshabilitar (DELETE)
    un usuario específico por su correo.
    """

    if request.method == 'GET':
        # 1. Llamar al selector de búsqueda
        usuario = list_users(correo=correo)
        if not usuario:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        # 2. Serializar y devolver
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        # 1. Llamar al selector de actualización
        #    update_user se encarga de extraer el password del 'data'
        updated_user = update_user(correo=correo, data=request.data)

        if not updated_user:
            return Response({"error": "Usuario no encontrado para actualizar"}, status=status.HTTP_404_NOT_FOUND)

        # 2. Serializar y devolver el usuario actualizado
        serializer = UsuarioSerializer(updated_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # 1. Llamar al selector de deshabilitación
        deactivated_user = deactivate_user_by_email(correo=correo)

        if not deactivated_user:
            return Response({"error": "Usuario no encontrado para deshabilitar"}, status=status.HTTP_404_NOT_FOUND)

        # 2. Devolver el usuario deshabilitado (o un 204 No Content)
        # Devolver el objeto es útil para confirmar el cambio de estado
        serializer = UsuarioSerializer(deactivated_user)
        return Response(serializer.data, status=status.HTTP_200_OK)

        # Alternativa: Devolver "Sin Contenido"
        # return Response(status=status.HTTP_204_NO_CONTENT)