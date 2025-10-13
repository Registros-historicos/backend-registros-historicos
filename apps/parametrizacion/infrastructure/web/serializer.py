from rest_framework import serializers

class ParametrizacionSerializer(serializers.Serializer):
    id_param = serializers.IntegerField()
    nombre = serializers.CharField()
    id_tema = serializers.IntegerField()
    id_param_padre = serializers.IntegerField(allow_null=True)
