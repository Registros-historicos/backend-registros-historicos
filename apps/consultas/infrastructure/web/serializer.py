
from rest_framework import serializers

class EntidadTopSerializer(serializers.Serializer):
    ent_federativa_param = serializers.IntegerField()
    entidad_nombre = serializers.CharField()
    total = serializers.IntegerField()

class StatusCountSerializer(serializers.Serializer):
    estatus = serializers.CharField()
    
class CategoriaInvestigadorSerializer(serializers.Serializer):
    categoria = serializers.CharField()
    total = serializers.IntegerField()

class InstitucionTopSerializer(serializers.Serializer):
    id_institucion = serializers.IntegerField()
    institucion_nombre = serializers.CharField()
    total = serializers.IntegerField()

class SectorEconomicoSerializer(serializers.Serializer):
    sector = serializers.CharField()
    total = serializers.IntegerField()
    
class RegistrosPorSexoSerializer(serializers.Serializer):
    sexo = serializers.CharField()
    total = serializers.IntegerField()