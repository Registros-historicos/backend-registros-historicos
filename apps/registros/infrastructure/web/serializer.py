from rest_framework import serializers

class RegistroSerializer(serializers.Serializer):
    no_expediente = serializers.CharField()
    titulo = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    descripcion = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    fec_solicitud = serializers.DateField(required=False, allow_null=True, input_formats=["%Y-%m-%d", "%d/%m/%Y"])
    no_titulo = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    estatus_param = serializers.IntegerField(required=False, allow_null=True)
    rama_param = serializers.IntegerField(required=False, allow_null=True)
    medio_ingreso_param = serializers.IntegerField(required=False, allow_null=True)
    tecnologico_origen = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    anio_renovacion = serializers.IntegerField(required=False, allow_null=True)
    id_subsector = serializers.IntegerField(required=False, allow_null=True)
    fec_expedicion = serializers.DateField(required=False, allow_null=True, input_formats=["%Y-%m-%d", "%d/%m/%Y"])
    archivo = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    observaciones = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    tipo_registro_param = serializers.IntegerField()
    tipo_ingreso_param = serializers.IntegerField()
    id_usuario = serializers.IntegerField()

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
