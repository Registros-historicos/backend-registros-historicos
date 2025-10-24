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

class RegistroListSerializer(serializers.Serializer):
    id_registro = serializers.IntegerField()
    no_expediente = serializers.CharField()
    titulo = serializers.CharField()
    tipo_ingreso_param = serializers.CharField()
    rama_param = serializers.CharField()
    estatus_param = serializers.CharField()
    tipo_registro_param = serializers.CharField()
    fec_solicitud = serializers.CharField()



class RegistrosSerializer(serializers.Serializer):
    id_registro = serializers.IntegerField(read_only=True)
    no_expediente = serializers.CharField()
    titulo = serializers.CharField()
    tipo_ingreso_param = serializers.CharField()
    id_usuarios = serializers.ListField(child=serializers.IntegerField())
    rama_param = serializers.CharField()
    fec_expedicion = serializers.CharField()
    observaciones = serializers.CharField()
    archivo = serializers.CharField()
    estatus_param = serializers.CharField()
    medio_ingreso_param = serializers.CharField()
    tipo_registro_param = serializers.CharField()
    fec_solicitud = serializers.CharField()
    descripcion = serializers.CharField()
    id_nstituciones = serializers.ListField(child=serializers.IntegerField())
    instituciones = serializers.ListField(child=serializers.CharField())
    
class PaginatedRegistroSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    page = serializers.IntegerField()
    limit = serializers.IntegerField()
    results = RegistrosSerializer(many=True)
