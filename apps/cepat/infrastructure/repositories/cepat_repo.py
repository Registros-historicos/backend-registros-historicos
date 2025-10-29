from rest_framework import serializers

class CepatSerializer(serializers.Serializer):
    """
    Serializador para MOSTRAR la entidad Cepat. (Salida)
    """
    id_cepat = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField(read_only=True)
    id_usuario = serializers.IntegerField(read_only=True)

class CepatInputSerializer(serializers.Serializer):
    """
    Serializador para VALIDAR la entrada al crear o actualizar un Cepat. (Entrada)
    """
    nombre = serializers.CharField(max_length=255, required=True)
    id_usuario = serializers.IntegerField(required=True)
