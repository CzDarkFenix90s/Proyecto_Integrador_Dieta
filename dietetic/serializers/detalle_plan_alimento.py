from rest_framework import serializers

from dietetic.models import (
    DetallePlanAlimento,
    PlanNutricional,
    AlimentoProgramado,
)

from dietetic.serializers.plan_nutricional import PlanNutricionalSerializer
from dietetic.serializers.alimento_programado import AlimentoProgramadoSerializer


class DetallePlanAlimentoResumenSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetallePlanAlimento
        fields = [
            'id',
            'quantity',
            'is_active',
        ]


class DetallePlanAlimentoSerializer(serializers.ModelSerializer):

    plan_nutricional = PlanNutricionalSerializer(read_only=True)
    plan_nutricional_id = serializers.PrimaryKeyRelatedField(
        source='plan_nutricional',
        write_only=True,
        queryset=PlanNutricional.objects.none(),
    )

    alimento_programado = AlimentoProgramadoSerializer(read_only=True)
    alimento_programado_id = serializers.PrimaryKeyRelatedField(
        source='alimento_programado',
        write_only=True,
        queryset=AlimentoProgramado.objects.none(),
    )

    has_observations = serializers.SerializerMethodField()

    class Meta:
        model = DetallePlanAlimento

        fields = [
            'id',
            'quantity',
            'observations',
            'has_observations',
            'is_active',

            'plan_nutricional',
            'plan_nutricional_id',

            'alimento_programado',
            'alimento_programado_id',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['plan_nutricional_id'].queryset = PlanNutricional.objects.filter(
            is_active=True
        )

        self.fields['alimento_programado_id'].queryset = AlimentoProgramado.objects.filter(
            is_active=True
        )

    def get_has_observations(self, obj):
        return obj.has_observations

    def validate_quantity(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                'La cantidad debe ser mayor que cero.'
            )

        return value