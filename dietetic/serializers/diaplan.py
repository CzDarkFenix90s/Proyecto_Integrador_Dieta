# dietetic/serializers/dia_plan.py

from rest_framework import serializers
from dietetic.models import DiaPlan


class DiaPlanSerializer(serializers.ModelSerializer):
    # Mostrar el nombre del plan al consultar
    plan_nutricional_nombre = serializers.CharField(
        source='plan_nutricional.nombre',
        read_only=True
    )

    class Meta:
        model = DiaPlan
        fields = [
            'id',
            'plan_nutricional',
            'plan_nutricional_nombre',
            'dia_semana',
            'descripcion',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        plan = attrs.get(
            'plan_nutricional',
            getattr(self.instance, 'plan_nutricional', None)
        )

        dia = attrs.get(
            'dia_semana',
            getattr(self.instance, 'dia_semana', None)
        )

        existe = DiaPlan.objects.filter(
            plan_nutricional=plan,
            dia_semana=dia
        )

        if self.instance:
            existe = existe.exclude(pk=self.instance.pk)

        if existe.exists():
            raise serializers.ValidationError(
                "Ese día ya existe para este plan nutricional."
            )

        return attrs