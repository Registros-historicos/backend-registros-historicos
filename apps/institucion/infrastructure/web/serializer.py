from rest_framework import serializers


class InstitucionSerializer(serializers.Serializer):
    """
    Serializa el dataclass Institucion para las respuestas de la API.
    """
    id_institucion = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField()
    ent_federativa_param = serializers.IntegerField(allow_null=True, required=False)
    tipo_institucion_param = serializers.IntegerField(allow_null=True, required=False)
    id_cepat = serializers.IntegerField(allow_null=True, required=False)
    ciudad_param = serializers.IntegerField(allow_null=True, required=False)

class UpdateIdCepatSerializer(serializers.Serializer):
    """
    Valida los datos de entrada para actualizar el id_cepat.
    """
    # required=False y allow_null=True permiten enviar {"id_cepat": null}
    id_cepat = serializers.IntegerField(required=False, allow_null=True)