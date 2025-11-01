from rest_framework import serializers

class InvestigadorSerializer(serializers.Serializer):
    id_investigador = serializers.IntegerField(read_only=True)
    nombre = serializers.CharField()
    ape_pat = serializers.CharField()
    ape_mat = serializers.CharField(allow_null=True, required=False)
    curp = serializers.CharField()
    sexo_param = serializers.IntegerField()
    tipo_investigador_param = serializers.IntegerField()


class AdscripcionSerializer(serializers.Serializer):
    id_adscripcion = serializers.IntegerField(read_only=True)
    id_investigador = serializers.IntegerField()
    id_institucion = serializers.IntegerField()
    departamento_param = serializers.IntegerField()
    programa_educativo_param = serializers.IntegerField()
    cuerpo_academico_param = serializers.IntegerField()
    fec_ini = serializers.DateTimeField()
    fec_fin = serializers.DateTimeField(allow_null=True, required=False)
