from rest_framework import serializers

class UsuarioCreateSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    ape_pat = serializers.CharField(max_length=100)
    ape_mat = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    url_foto = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    correo = serializers.EmailField(max_length=150)
    password = serializers.CharField(write_only=True)  # raw
    telefono = serializers.CharField(max_length=15, required=False, allow_null=True, allow_blank=True)
    tipo_usuario_param = serializers.IntegerField()
    estatus = serializers.IntegerField(default=1)

class UsuarioUpdateSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    ape_pat = serializers.CharField(max_length=100)
    ape_mat = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    url_foto = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    correo = serializers.EmailField(max_length=150)
    new_password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    telefono = serializers.CharField(max_length=15, required=False, allow_null=True, allow_blank=True)
    tipo_usuario_param = serializers.IntegerField()
    estatus = serializers.IntegerField()

class UsuarioResponseSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField()
    nombre = serializers.CharField()
    ape_pat = serializers.CharField()
    ape_mat = serializers.CharField(allow_null=True, required=False)
    url_foto = serializers.CharField(allow_null=True, required=False)
    correo = serializers.EmailField()
    telefono = serializers.CharField(allow_null=True, required=False)
    tipo_usuario_param = serializers.IntegerField()
    estatus = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

class EntidadTopSerializer(serializers.Serializer):
    ent_federativa_param = serializers.IntegerField()
    entidad_nombre = serializers.CharField()
    total = serializers.IntegerField()