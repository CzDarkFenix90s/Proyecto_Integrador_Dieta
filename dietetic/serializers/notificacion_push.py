from rest_framework import serializers
from dietetic.models import NotificacionPush


class NotificacionPushSerializer(serializers.ModelSerializer):
    paciente_id = serializers.PrimaryKeyRelatedField(
        source="paciente",
        read_only=True
    )

    class Meta:
        model = NotificacionPush
        fields = [
            "id",
            "paciente_id",
            "titulo",
            "mensaje",
            "leido",
            "fecha_envio",
        ]
        read_only_fields = [
            "id",
            "fecha_envio",
        ]

    def validate_titulo(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "El título no puede estar vacío."
            )
        return value

    def validate_mensaje(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "El mensaje no puede estar vacío."
            )
        return value

    def validate(self, attrs):
        titulo = attrs.get("titulo", "")
        mensaje = attrs.get("mensaje", "")

        if len(titulo) > 100:
            raise serializers.ValidationError({
                "titulo": "El título no puede superar los 100 caracteres."
            })

        if len(mensaje) > 1000:
            raise serializers.ValidationError({
                "mensaje": "El mensaje no puede superar los 1000 caracteres."
            })

        return attrs

    def create(self, validated_data):
        return NotificacionPush.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.titulo = validated_data.get("titulo", instance.titulo)
        instance.mensaje = validated_data.get("mensaje", instance.mensaje)
        instance.leido = validated_data.get("leido", instance.leido)
        instance.save()
        return instance