# dietetic/views/categoria_alimento.py

from rest_framework import viewsets

from dietetic.models import CategoriaAlimento
from dietetic.serializers.categoria_alimento import CategoriaAlimentoSerializer
from dietetic.permissions import IsStaffOrReadOnly
from dietetic.pagination import StandardPagination


class CategoriaAlimentoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaAlimento.objects.all()
    serializer_class = CategoriaAlimentoSerializer
    pagination_class = StandardPagination

    filterset_fields = [
        'estado',
    ]

    search_fields = [
        'nombre',
        'descripcion',
    ]

    ordering_fields = [
        'id',
        'nombre',
        'created_at',
    ]

    ordering = ['nombre']

    permission_classes = [IsStaffOrReadOnly]