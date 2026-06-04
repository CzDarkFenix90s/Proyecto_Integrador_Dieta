# dietetic/serializers/paciente.py
from rest_framework import serializers
from dietetic.models import Paciente, SeguimientoNutricional
from decimal import Decimal
from django.contrib.auth.models import User


class SeguimientoNutricionalSerializer(serializers.ModelSerializer):
    paciente_id = serializers.PrimaryKeyRelatedField(source='paciente', read_only=True)

    class Meta:
        model  = SeguimientoNutricional
        fields = ['id', 'paciente_id', 'weight_kg', 'waist_cm', 'notes', 'created_at']
        read_only_fields = ['id', 'created_at']


class PacienteSerializer(serializers.ModelSerializer):
    num_seguimientos = serializers.SerializerMethodField()
    seguimientos = SeguimientoNutricionalSerializer(many=True, read_only=True)
    user_id = serializers.IntegerField(required=False, write_only=True)

    class Meta:
        model  = Paciente
        fields = [
            'id', 'user_id', 'patient_code', 'full_name', 'age', 'goal',
            'dietary_restrictions', 'current_weight', 'height_cm',
            'status', 'medical_notes', 'bmi', 'num_seguimientos',
            'seguimientos', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_num_seguimientos(self, obj):
        return obj.seguimientos.count()

    def create(self, validated_data):
        user_id = validated_data.pop('user_id', None)
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                validated_data['user'] = user
            except User.DoesNotExist:
                pass
        return super().create(validated_data)


class AddSeguimientoNutricionalSerializer(serializers.Serializer):
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
