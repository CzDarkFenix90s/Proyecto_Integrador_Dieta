from rest_framework import serializers
from dietetic.models import FacturaPago


class FacturaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaPago
        fields = [
            'id',
            'paciente',
            'consulta',
            'invoice_number',
            'payment_method',
            'total_amount',
            'payment_date',
            'status',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]