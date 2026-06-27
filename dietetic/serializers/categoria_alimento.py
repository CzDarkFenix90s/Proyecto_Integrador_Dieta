# dietetic/serializers/categoria_alimento.py

from rest_framework import serializers
from dietetic.models import CategoriaAlimento


class CategoriaAlimentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoriaAlimento
        fields = [
            'id',
            'nombre',
            'descripcion',
            'estado',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]

    def validate_nombre(self, value):
        value = value.strip()

        existe = CategoriaAlimento.objects.filter(
            nombre__iexact=value
        )

        if self.instance:
            existe = existe.exclude(pk=self.instance.pk)

        if existe.exists():
            raise serializers.ValidationError(
                "Ya existe una categoría con ese nombre."
            )

        return value