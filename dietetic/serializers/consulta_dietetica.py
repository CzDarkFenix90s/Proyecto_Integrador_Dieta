from rest_framework import serializers
from dietetic.models import ConsultaDietetica, PlanNutricional, Nutricionista, Paciente
from dietetic.serializers.plan_nutricional import PlanNutricionalSerializer



class ConsultaDieteticaSerializer(serializers.ModelSerializer):
    # Definimos los campos como llaves primarias (IDs) para recibir datos en POST/PUT
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
            'duration_minutes', 'is_delayed', 'created_at',
        ]

    def get_duration_minutes(self, obj):
        return obj.duration_minutes

    def get_is_delayed(self, obj):
        return obj.is_delayed

    def to_representation(self, instance):
        """
        Transforma los IDs numéricos en objetos detallados al enviar la respuesta (GET).
        """
        # 1. Obtiene la representación estándar (donde estos campos son solo IDs)
        representation = super().to_representation(instance)
        
        # 2. Reemplaza los IDs con los datos completos usando los serializadores detallados
        if instance.plan_nutricional:
            representation['plan_nutricional'] = PlanNutricionalSerializer(instance.plan_nutricional).data
            
        return representation
