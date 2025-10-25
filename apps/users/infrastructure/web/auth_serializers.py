from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    correo = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    access_exp = serializers.DateTimeField()
    refresh = serializers.CharField()
    refresh_exp = serializers.DateTimeField()
    user = serializers.DictField()

class RefreshRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class RefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    access_exp = serializers.DateTimeField()
