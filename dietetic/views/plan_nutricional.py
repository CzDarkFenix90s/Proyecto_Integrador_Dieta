# dietetic/views/plan_nutricional.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from dietetic.models import PlanNutricional
from dietetic.serializers.plan_nutricional import PlanNutricionalSerializer
from dietetic.permissions import IsStaffOrReadOnly
from dietetic.pagination import StandardPagination


class PlanNutricionalViewSet(viewsets.ModelViewSet):
    queryset           = PlanNutricional.objects.all()
    serializer_class   = PlanNutricionalSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields   = ['is_active']
    search_fields      = ['name', 'goal', 'description']
    ordering_fields    = ['name', 'created_at', 'estimated_cost']
    ordering           = ['name']

    @action(detail=True, methods=['get'], url_path='alimentos')
    def active_alimentos(self, request, pk=None):
        from dietetic.models import AlimentoProgramado
        from dietetic.serializers.alimento_programado import AlimentoResumenSerializer
        plan = self.get_object()
        qs   = plan.alimentos.filter(is_active=True).order_by('sequence')
        page = self.paginate_queryset(qs)
        if page is not None:
            return self.get_paginated_response(
                AlimentoResumenSerializer(page, many=True).data
            )
        return Response(AlimentoResumenSerializer(qs, many=True).data)

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        qs = PlanNutricional.objects.annotate(num_alimentos=Count('alimentos', distinct=True))
        return Response({
            'total':    qs.count(),
            'active':   qs.filter(is_active=True).count(),
            'inactive': qs.filter(is_active=False).count(),
            'detail': [
                {
                    'id':          plan.id,
                    'name':         plan.name,
                    'num_alimentos': plan.num_alimentos,
                    'is_active':    plan.is_active,
                }
                for plan in qs.order_by('name')
            ],
        })
