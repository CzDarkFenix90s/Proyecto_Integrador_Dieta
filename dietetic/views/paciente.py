from rest_framework import viewsets, permissions
from dietetic.models import Paciente, SeguimientoNutricional
from dietetic.serializers.paciente import (
    PacienteSerializer,
    SeguimientoNutricionalSerializer,
)
from dietetic.permissions import IsStaffOrReadOnly
from dietetic.pagination import StandardPagination


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    pagination_class = StandardPagination
    filterset_fields = ['status']
    search_fields = ['patient_code', 'full_name', 'goal']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [IsStaffOrReadOnly()]


class SeguimientoNutricionalViewSet(viewsets.ModelViewSet):
    queryset = SeguimientoNutricional.objects.all()
    serializer_class = SeguimientoNutricionalSerializer
    pagination_class = StandardPagination
    permission_classes = [IsStaffOrReadOnly]

    filterset_fields = ['paciente']
    search_fields = ['paciente__full_name']