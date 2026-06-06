# dietetic/serializers/nutricionista.py
from rest_framework import serializers
from dietetic.models import Nutricionista
from django.contrib.auth.models import User


class NutricionistaSerializer(serializers.ModelSerializer):
    full_name        = serializers.SerializerMethodField()
    fee_with_bonus   = serializers.SerializerMethodField()
    is_experienced   = serializers.SerializerMethodField()

    # Campos para creación de cuenta de usuario
    username = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model  = Nutricionista
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'professional_id',
            'specialty', 'consultation_fee', 'fee_with_bonus', 'consultations_completed',
            'is_experienced', 'is_active', 'created_at',
            'username', 'email', 'password'
        ]
        read_only_fields = ['id', 'created_at']

    def get_full_name(self, obj):
        return obj.full_name

    def get_fee_with_bonus(self, obj):
        return obj.fee_with_bonus

    def get_is_experienced(self, obj):
        return obj.is_experienced

    def create(self, validated_data):
        username = validated_data.pop('username', None)
        email = validated_data.pop('email', None)
        password = validated_data.pop('password', None)

        user = None
        if username and password:
            # Crear el usuario de Django
            user = User.objects.create_user(
                username=username,
                email=email or "",
                password=password,
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', '')
            )

        nutricionista = Nutricionista.objects.create(user=user, **validated_data)
        return nutricionista
