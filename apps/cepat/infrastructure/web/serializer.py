from rest_framework import serializers

class CepatSerializer(serializers.Serializer):
    """
    Serializador para MOSTRAR la entidad Cepat. (Salida)
    Se usa para convertir el dataclass Cepat a JSON.
    """
    id_cepat = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(read_only=True)
    id_usuario = serializers.IntegerField(read_only=True)

class CepatInputSerializer(serializers.Serializer):
    """
    Serializador para VALIDAR la entrada al crear o actualizar un Cepat. (Entrada)
    Se usa para validar el 'request.data' de la vista.
    """
    nombre = serializers.CharField(max_length=255, required=True)
    id_usuario = serializers.IntegerField(required=True)

