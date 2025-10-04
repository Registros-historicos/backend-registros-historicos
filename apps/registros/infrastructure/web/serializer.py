from rest_framework import serializers

class RegistroSerializer(serializers.Serializer):
    id_registro = serializers.IntegerField(read_only=True)
    no_expediente = serializers.CharField()
    titulo = serializers.CharField()
    tipo_ingreso_param = serializers.CharField()
    id_usuario = serializers.IntegerField()
    rama_param = serializers.CharField()
    fec_expedicion = serializers.CharField()
    observaciones = serializers.CharField()
    archivo = serializers.CharField()
    estatus_param = serializers.CharField()
    medio_ingreso_param = serializers.CharField()
    tipo_registro_param = serializers.CharField()
    fec_solicitud = serializers.CharField()
    descripcion = serializers.CharField()
    tipo_sector_param = serializers.CharField()
