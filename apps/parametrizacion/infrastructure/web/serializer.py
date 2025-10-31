from rest_framework import serializers

class ParametrizacionSerializer(serializers.Serializer):
    id_param = serializers.IntegerField()
    nombre = serializers.CharField()
    id_tema = serializers.IntegerField()
    id_param_padre = serializers.IntegerField(allow_null=True)

class EstadoSerializer(serializers.Serializer):
    id_entidad_federativa = serializers.IntegerField()
    nombre_entidad = serializers.CharField(max_length=255)

class InstitucionPorEstadoSerializer(serializers.Serializer):
    id_institucion = serializers.IntegerField()
    nombre_institucion = serializers.CharField()
    nombre_entidad_federativa = serializers.CharField()