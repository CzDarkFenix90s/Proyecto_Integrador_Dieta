# dietetic/views/nutricionista.py
from rest_framework import viewsets
from dietetic.models import Nutricionista
from dietetic.serializers.nutricionista import NutricionistaSerializer
from dietetic.permissions import IsStaffOrReadOnly
from dietetic.pagination import StandardPagination


class NutricionistaViewSet(viewsets.ModelViewSet):
    queryset           = Nutricionista.objects.all()
    serializer_class   = NutricionistaSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class   = StandardPagination
    filterset_fields   = ['is_active']
    search_fields      = ['first_name', 'last_name', 'professional_id', 'specialty']
