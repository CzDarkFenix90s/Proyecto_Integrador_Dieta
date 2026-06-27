# dietetic/views/dia_plan.py

from rest_framework import viewsets

from dietetic.models import DiaPlan
from dietetic.serializers.diaplan import DiaPlanSerializer
from dietetic.permissions import IsStaffOrReadOnly
from dietetic.pagination import StandardPagination


class DiaPlanViewSet(viewsets.ModelViewSet):
    queryset = DiaPlan.objects.all()
    serializer_class = DiaPlanSerializer
    pagination_class = StandardPagination

    filterset_fields = [
        'plan_nutricional',
        'dia_semana',
    ]

    search_fields = [
        'dia_semana',
        'descripcion',
        'plan_nutricional__nombre',
    ]

    ordering_fields = [
        'id',
        'dia_semana',
        'created_at',
    ]

    ordering = ['id']

    permission_classes = [IsStaffOrReadOnly]