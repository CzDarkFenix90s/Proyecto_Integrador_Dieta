from rest_framework import serializers
from dietetic.models import PerfilUsuario


class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = [
            'id',
            'user',
            'phone',
            'address',
            'role',
            'profile_photo',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]