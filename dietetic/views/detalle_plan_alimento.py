from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count

from dietetic.models import DetallePlanAlimento
from dietetic.serializers.detalle_plan_alimento import (
    DetallePlanAlimentoSerializer,
    DetallePlanAlimentoResumenSerializer,
)

from dietetic.permissions import IsStaffOrReadOnly
from dietetic.pagination import StandardPagination


class DetallePlanAlimentoViewSet(viewsets.ModelViewSet):

    queryset = DetallePlanAlimento.objects.select_related(
        'plan_nutricional',
        'alimento_programado',
    ).all()

    serializer_class = DetallePlanAlimentoSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class = StandardPagination

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        'is_active',
        'plan_nutricional',
        'alimento_programado',
    ]

    search_fields = [
        'plan_nutricional__name',
        'alimento_programado__name',
        'observations',
    ]

    ordering_fields = [
        'quantity',
        'created_at',
    ]

    ordering = [
        'created_at',
    ]

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[AllowAny],
        url_path='available',
    )
    def available(self, request):

        qs = self.filter_queryset(
            self.get_queryset().filter(is_active=True)
        )

        page = self.paginate_queryset(qs)

        if page is not None:
            return self.get_paginated_response(
                DetallePlanAlimentoResumenSerializer(
                    page,
                    many=True
                ).data
            )

        return Response(
            DetallePlanAlimentoResumenSerializer(
                qs,
                many=True
            ).data
        )

    @action(
        detail=False,
        methods=['get'],
        url_path='stats',
    )
    def stats(self, request):

        qs = DetallePlanAlimento.objects.all()

        data = qs.aggregate(
            total_active=Count('id'),
            avg_quantity=Avg('quantity'),
        )

        data['total_inactive'] = qs.filter(
            is_active=False
        ).count()

        if data['avg_quantity']:
            data['avg_quantity'] = round(
                float(data['avg_quantity']),
                2,
            )

        return Response(data)