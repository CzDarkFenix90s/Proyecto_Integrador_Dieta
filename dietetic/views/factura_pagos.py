# dietetic/views/factura_pago.py

from rest_framework import viewsets
from dietetic.models import FacturaPago
from dietetic.serializers.factura_pagos import FacturaPagoSerializer
from dietetic.permissions import IsStaffOrReadOnly
from dietetic.pagination import StandardPagination


class FacturaPagoViewSet(viewsets.ModelViewSet):
    queryset = FacturaPago.objects.all()
    serializer_class = FacturaPagoSerializer
    pagination_class = StandardPagination
    permission_classes = [IsStaffOrReadOnly]

    filterset_fields = [
        'status',
        'payment_method',
        'payment_date',
    ]

    search_fields = [
        'invoice_number',
        'paciente__full_name',
    ]

    ordering_fields = [
        'payment_date',
        'total_amount',
        'created_at',
    ]

    ordering = ['-payment_date']