from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied
from apps.users.application.selectors.get_all_users import get_all_users
from apps.users.application.selectors.get_user_by_email import list_users
from apps.users.application.selectors.create_user import create_new_user
from apps.users.application.selectors.update_user_by_email import update_user
from apps.users.application.selectors.deactivate_user_by_email import deactivate_user_by_email
from .serializer import UsuarioSerializer, UserCreateSerializer
from ...application.selectors.delate_user_by_id import delete_users_by_id
from ...application.selectors.get_users_by_type import get_users_by_type_list
from ...domain.entities import Usuario
from django.contrib.auth.hashers import make_password


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def list_create_users_view(request):
    """
    Vista para Listar todos los usuarios (GET) o Crear uno nuevo (POST).
    """
    if request.method == 'GET':
        usuarios_list = get_all_users(request.user)

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

            new_user_obj = create_new_user(
                request.user,
                user_entity,
                make_password(raw_password)
            )

            if not new_user_obj:
                return Response({"error": "No se pudo crear el usuario."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            response_serializer = UsuarioSerializer(new_user_obj)

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)


        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except IntegrityError:
            return Response({"error": f"El correo '{data['correo']}' ya existe."}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({"error": f"Error inesperado al crear usuario: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail_update_delete_view(request, correo: str):
    """
    Vista para Obtener (GET), Actualizar (PUT) o Deshabilitar (DELETE)
    un usuario específico por su correo.
    """

    if request.method == 'GET':
        usuario = list_users(correo=correo, user=request.user)
        if not usuario:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        try:
            updated_user = update_user(request.user, correo=correo, data=request.data)
            if not updated_user:
                return Response({"error": "Usuario no encontrado para actualizar"}, status=status.HTTP_404_NOT_FOUND)
            serializer = UsuarioSerializer(updated_user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": f"Error inesperado al actualizar: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'DELETE':
        try:
            deactivated_user = deactivate_user_by_email(correo, request.user)
            if not deactivated_user:
                return Response({"error": "Usuario no encontrado para deshabilitar"}, status=status.HTTP_404_NOT_FOUND)
            serializer = UsuarioSerializer(deactivated_user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({"error": f"Error inesperado al deshabilitar: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MeView(APIView):
    """
    Devuelve los datos del usuario autenticado (según el JWT).
    (Este código no necesita cambios)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u = request.user
        data = {
            "id_usuario": getattr(u, "id_usuario", getattr(u, "id", None)) or getattr(u, "sub", None),
            "correo": getattr(u, "correo", getattr(u, "email", None)),
            "tipo_usuario_param": getattr(u, "tipo_usuario_param", None),
            "nombre": getattr(u, "nombre", None),
        }

        claims = getattr(request, "auth", None)
        if isinstance(claims, dict):
            data["id_usuario"] = data["id_usuario"] or claims.get("sub")
            data["correo"] = data["correo"] or claims.get("correo")
            data["tipo_usuario_param"] = data["tipo_usuario_param"] or claims.get("tipo_usuario_param")
            data["nombre"] = data.get("nombre") or claims.get("nombre")

        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_by_type_view(request, tipo: int):
    """
    Vista para Obtener una LISTA de usuarios por su tipo (GET).
    """
    if request.method == 'GET':
        usuarios_list = get_users_by_type_list(tipo, request.user)
        serializer = UsuarioSerializer(usuarios_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def user_delate_by_id_view(request, id_user: int):
    """
    Vista para eliminar a un usuario específico por su ID (DELETE).
    (Se conserva el 'delate' original)
    """
    if request.method == 'DELETE':
        try:
            delete_users_by_id(id_user, request.user)

        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        except RuntimeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "Usuario eliminado correctamente"}, status=status.HTTP_200_OK)
#AGREGADO
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_completo_view(request):
    """
    Endpoint para obtener el perfil COMPLETO del usuario autenticado
    """
    try:
        # Obtener ID del usuario autenticado
        user_id = getattr(request.user, "id", getattr(request.user, "sub", None))
        if not user_id:
            return Response({"error": "Usuario no identificado"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Usar el selector existente adaptado
        from apps.users.application.selectors.get_user_by_id import get_user_profile_completo
        perfil = get_user_profile_completo(int(user_id), request.user)
        
        if not perfil:
            return Response({"error": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(perfil, status=status.HTTP_200_OK)
        
    except PermissionDenied as e:
        return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
    except Exception as e:
        return Response({"error": f"Error obteniendo perfil: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
