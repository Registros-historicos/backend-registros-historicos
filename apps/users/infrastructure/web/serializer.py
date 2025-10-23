from rest_framework import serializers
from apps.users.domain.entities import Usuario

class UsuarioSerializer(serializers.Serializer):
    """
    Serializa el dataclass Usuario para las respuestas de la API.
    """
    id_usuario = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField()
    ape_pat = serializers.CharField()
    ape_mat = serializers.CharField(allow_null=True)
    url_foto = serializers.CharField(allow_null=True, required=False)
    correo = serializers.EmailField()
    telefono = serializers.CharField(allow_null=True, required=False)
    tipo_usuario_param = serializers.IntegerField()
    estatus = serializers.IntegerField()
    # created_at = serializers.DateTimeField(read_only=True)
    # updated_at = serializers.DateTimeField(read_only=True)

    # Nota: Como Usuario es un dataclass, este serializador se usa
    # principalmente para *serializar* (convertir a JSON) datos
    # que vienen de los selectores, no para *deserializar* (crear instancias).
    # Los datos de entrada (request.data) se pasan como dict a los selectores.


class UserCreateSerializer(serializers.Serializer):
    """
    Valida los datos de entrada para la creación de un nuevo usuario.
    """
    nombre = serializers.CharField(max_length=100)
    ape_pat = serializers.CharField(max_length=100)
    ape_mat = serializers.CharField(max_length=100, allow_null=True, required=False)
    correo = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8) # write_only para que no se muestre en la respuesta
    telefono = serializers.CharField(max_length=20, allow_null=True, required=False)
    tipo_usuario_param = serializers.IntegerField()
    estatus = serializers.IntegerField(default=1, required=False)
    url_foto = serializers.CharField(allow_null=True, required=False)