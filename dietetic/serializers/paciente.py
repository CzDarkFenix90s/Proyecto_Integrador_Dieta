from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework import serializers
from dietetic.models.paciente import Paciente
from dietetic.models.user_profile import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    paciente_id = serializers.PrimaryKeyRelatedField(source='paciente', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'paciente_id', 'weight_kg', 'waist_cm', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


# Alias para mantener la compatibilidad con otras partes que busquen el nombre anterior
SeguimientoNutricionalSerializer = UserProfileSerializer


class PacienteSerializer(serializers.ModelSerializer):
    num_seguimientos = serializers.SerializerMethodField()
    seguimientos = UserProfileSerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Paciente
        fields = [
            'id', 'user_id', 'patient_code', 'first_name', 'last_name', 'full_name',
            'age', 'goal', 'dietary_restrictions', 'current_weight', 'height_cm',
            'status', 'medical_notes', 'bmi', 'num_seguimientos',
            'seguimientos', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_num_seguimientos(self, obj):
        try:
            return obj.seguimientos.count()
        except AttributeError:
            return 0

    def get_full_name(self, obj):
        return getattr(obj, 'full_name', f"{obj.first_name} {obj.last_name}")

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = None
        if request and 'user_id' in request.data:
            user_id = request.data.get('user_id')

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                validated_data['user'] = user
                if not validated_data.get('first_name'):
                    validated_data['first_name'] = user.first_name
                if not validated_data.get('last_name'):
                    validated_data['last_name'] = user.last_name
            except User.DoesNotExist:
                pass
        return super().create(validated_data)


class AddUserProfileSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    weight_kg  = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=Decimal('1.00'))
    waist_cm   = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)
    notes      = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_patient_id(self, value):
        try:
            Paciente.objects.get(pk=value, status='activo')
        except Paciente.DoesNotExist:
            raise serializers.ValidationError(
                f'Paciente con ID {value} no encontrado o no está activo.'
            )
        return value