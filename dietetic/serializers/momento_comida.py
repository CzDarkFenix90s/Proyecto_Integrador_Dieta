# dietetic/serializers/momento_comida.py

from rest_framework import serializers
from dietetic.models import MomentoComida


class MomentoComidaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MomentoComida
        fields = '__all__'
        read_only_fields = ['id', 'created_at']