# dietetic/views/momento_comida.py

from rest_framework import viewsets

from dietetic.models import MomentoComida
from dietetic.serializers.momento_comida import MomentoComidaSerializer
from dietetic.permissions import IsStaffOrReadOnly
from dietetic.pagination import StandardPagination


class MomentoComidaViewSet(viewsets.ModelViewSet):
    queryset = MomentoComida.objects.all()
    serializer_class = MomentoComidaSerializer
    pagination_class = StandardPagination

    filterset_fields = ['nombre']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['id', 'nombre', 'created_at']
    ordering = ['id']

    permission_classes = [IsStaffOrReadOnly]