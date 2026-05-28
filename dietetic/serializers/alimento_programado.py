# dietetic/serializers/alimento_programado.py
from rest_framework import serializers
from dietetic.models import AlimentoProgramado, PlanNutricional
from dietetic.serializers.plan_nutricional import PlanNutricionalSerializer


class AlimentoResumenSerializer(serializers.ModelSerializer):

    class Meta:
        model  = AlimentoProgramado
        fields = ['id', 'name', 'meal_type', 'portion_grams', 'sequence', 'is_active']


class AlimentoProgramadoSerializer(serializers.ModelSerializer):
    plan_nutricional = PlanNutricionalSerializer(read_only=True)
    plan_nutricional_id = serializers.PrimaryKeyRelatedField(
        source='plan_nutricional',
        write_only=True,
        queryset=PlanNutricional.objects.none(),
    )
    estimated_preparation_minutes = serializers.SerializerMethodField()
    has_sequence = serializers.SerializerMethodField()

    class Meta:
        model  = AlimentoProgramado
        fields = [
            'id', 'name', 'description', 'meal_type', 'portion_grams',
            'estimated_preparation_minutes', 'sequence', 'has_sequence', 'is_active',
            'plan_nutricional', 'plan_nutricional_id', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from dietetic.models import PlanNutricional
        self.fields['plan_nutricional_id'].queryset = PlanNutricional.objects.filter(is_active=True)

    def get_estimated_preparation_minutes(self, obj):
        return obj.estimated_preparation_minutes

    def get_has_sequence(self, obj):
        return obj.has_sequence

    def validate_portion_grams(self, value):
        if value <= 0:
            raise serializers.ValidationError('La porción debe ser mayor que 0 gramos.')
        return value

    def validate_sequence(self, value):
        if value < 0:
            raise serializers.ValidationError('La secuencia no puede ser negativa.')
        return value
