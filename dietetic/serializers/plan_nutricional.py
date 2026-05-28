# dietetic/serializers/plan_nutricional.py
from rest_framework import serializers
from dietetic.models import PlanNutricional


class PlanNutricionalSerializer(serializers.ModelSerializer):
    total_alimentos = serializers.SerializerMethodField()

    class Meta:
        model  = PlanNutricional
        fields = [
            'id', 'name', 'description', 'goal', 'target_calories',
            'duration_weeks', 'estimated_cost', 'is_active', 'total_alimentos', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def get_total_alimentos(self, obj):
        return obj.alimentos.filter(is_active=True).count()

    def validate_name(self, value):
        qs = PlanNutricional.objects.filter(name__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError('Ya existe un plan nutricional con este nombre.')
        return value
