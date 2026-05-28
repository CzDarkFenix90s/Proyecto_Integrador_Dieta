# dietetic/serializers/consulta_dietetica.py
from rest_framework import serializers
from dietetic.models import ConsultaDietetica
from dietetic.serializers.plan_nutricional import PlanNutricionalSerializer
from dietetic.serializers.nutricionista import NutricionistaSerializer


class ConsultaDieteticaSerializer(serializers.ModelSerializer):
    plan_nutricional  = PlanNutricionalSerializer(read_only=True)
    nutricionista      = NutricionistaSerializer(read_only=True)
    paciente_nombre    = serializers.CharField(source='paciente.full_name', read_only=True)
    duration_minutes   = serializers.SerializerMethodField()
    is_delayed         = serializers.SerializerMethodField()

    class Meta:
        model  = ConsultaDietetica
        fields = [
            'id', 'status', 'session_notes', 'scheduled_time', 'estimated_end',
            'duration_minutes', 'is_delayed', 'plan_nutricional', 'nutricionista',
            'paciente_nombre', 'created_at',
        ]

    def get_duration_minutes(self, obj):
        return obj.duration_minutes

    def get_is_delayed(self, obj):
        return obj.is_delayed
