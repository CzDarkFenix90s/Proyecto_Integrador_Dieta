# dietetic/views/paciente.py
from rest_framework import viewsets, permissions
from dietetic.models import Paciente
from dietetic.serializers.paciente import PacienteSerializer
from dietetic.permissions import IsStaffOrReadOnly
from dietetic.pagination import StandardPagination


class PacienteViewSet(viewsets.ModelViewSet):
    queryset           = Paciente.objects.all()
    serializer_class   = PacienteSerializer
    pagination_class   = StandardPagination
    filterset_fields   = ['status']
    search_fields      = ['patient_code', 'full_name', 'goal']

    def get_permissions(self):
        if self.action == 'create':
            # Permitir a cualquier usuario autenticado crear su perfil de paciente
            return [permissions.IsAuthenticated()]
        return [IsStaffOrReadOnly()]
