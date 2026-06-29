from rest_framework import serializers
from dietetic.models import RutinaEjercicio
from dietetic.models.plan_nutricional import PlanNutricional


class RutinaEjercicioSerializer(serializers.ModelSerializer):
    plan_nutricional_id = serializers.PrimaryKeyRelatedField(source='plan_nutricional',queryset=PlanNutricional.objects.all())

    class Meta:
        model = RutinaEjercicio
        fields = [
            'id', 'plan_nutricional_id', 'descripcion_rutina',
            'dias_semana', 'duracion_minutos', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']