from rest_framework import serializers
from dietetic.models import ConsultaDietetica, PlanNutricional, Nutricionista, Paciente
from dietetic.serializers.plan_nutricional import PlanNutricionalSerializer
from dietetic.serializers.nutricionista import NutricionistaSerializer


class ConsultaDieteticaSerializer(serializers.ModelSerializer):
    # Campos para lectura detallada
    plan_nutricional_detail = PlanNutricionalSerializer(source='plan_nutricional', read_only=True)
    nutricionista_detail = NutricionistaSerializer(source='nutricionista', read_only=True)
    paciente_nombre = serializers.CharField(source='paciente.full_name', read_only=True)

    # Campos para escritura (IDs)
    plan_nutricional = serializers.PrimaryKeyRelatedField(queryset=PlanNutricional.objects.all())
    nutricionista = serializers.PrimaryKeyRelatedField(queryset=Nutricionista.objects.all())
    paciente = serializers.PrimaryKeyRelatedField(queryset=Paciente.objects.all())

    duration_minutes = serializers.SerializerMethodField()
    is_delayed = serializers.SerializerMethodField()

    class Meta:
        model = ConsultaDietetica
        fields = [
            'id', 'status', 'session_notes', 'scheduled_time', 'estimated_end',
            'plan_nutricional', 'nutricionista', 'paciente',
            'paciente_nombre', 'plan_nutricional_detail', 'nutricionista_detail',
            'duration_minutes', 'is_delayed', 'created_at',
        ]

    def get_duration_minutes(self, obj):
        return obj.duration_minutes

    def get_is_delayed(self, obj):
        return obj.is_delayed
