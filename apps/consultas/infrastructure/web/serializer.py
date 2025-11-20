
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

class InstitucionAllSerializer(serializers.Serializer):
    id_institucion = serializers.IntegerField()
    institucion_nombre = serializers.CharField()
    tipo_institucion = serializers.CharField()
    total = serializers.IntegerField()

class InvestigadorPorCoordinadorSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    departamento = serializers.CharField()
    solicitudes = serializers.IntegerField()

class UsuarioPorEstadoCepatSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField()
    nombre = serializers.CharField()
    ape_pat = serializers.CharField()
    ape_mat = serializers.CharField(required=False, allow_null=True)
    url_foto = serializers.CharField(required=False, allow_null=True)
    correo = serializers.EmailField()
    telefono = serializers.CharField()
    tipo_usuario_param = serializers.IntegerField()
    estatus_param = serializers.IntegerField()
    id_institucion = serializers.IntegerField()
    nombre_institucion = serializers.CharField()

class ProgramaEducativoSerializer(serializers.Serializer):
    programa_educativo_param = serializers.IntegerField()
    nombre_programa_educativo = serializers.CharField(max_length=255)
    total = serializers.IntegerField()

class RegistrosPorProgramaSerializer(serializers.Serializer):
    programa_educativo = serializers.CharField()
    total_registros = serializers.IntegerField()
