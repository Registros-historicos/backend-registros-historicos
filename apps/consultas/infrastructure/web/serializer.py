
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

class RequestTypeSerializer(serializers.Serializer):
    tipo_registro = serializers.CharField()
    rama = serializers.CharField()
    total = serializers.IntegerField()

class SectorActividadSerializer(serializers.Serializer):
    sector_nombre = serializers.CharField()
    actividad_nombre = serializers.CharField()
    total = serializers.IntegerField()

class RegistrosPorMesSerializer(serializers.Serializer):
    mes = serializers.IntegerField()
    total = serializers.IntegerField()

class RegistrosPorPeriodoSerializer(serializers.Serializer):
    anio = serializers.IntegerField()
    mes = serializers.IntegerField()
    tipo_registro_param = serializers.IntegerField()
    total = serializers.IntegerField()
