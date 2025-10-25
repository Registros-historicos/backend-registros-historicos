from rest_framework import serializers


class InstitucionSerializer(serializers.Serializer):
    """
    Serializa el dataclass Institucion para las respuestas de la API.
    """
    id_institucion = serializers.IntegerField(read_only=True)
    id_cepat = serializers.IntegerField(allow_null=True)
    nombre = serializers.CharField()
    clave = serializers.CharField()
    direccion = serializers.CharField(allow_null=True)
    estatus = serializers.IntegerField(source='estatus_param', required=False)


class UpdateIdCepatSerializer(serializers.Serializer):
    """
    Valida los datos de entrada para actualizar el id_cepat.
    """
    # required=False y allow_null=True permiten enviar {"id_cepat": null}
    id_cepat = serializers.IntegerField(required=False, allow_null=True)