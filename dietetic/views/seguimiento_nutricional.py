# dietetic/views/seguimiento_nutricional.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from dietetic.models import SeguimientoNutricional
from dietetic.serializers import SeguimientoNutricionalSerializer


class SeguimientoNutricionalViewSet(viewsets.ModelViewSet):
    queryset = SeguimientoNutricional.objects.all()
    serializer_class = SeguimientoNutricionalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = SeguimientoNutricional.objects.all()

        paciente = self.request.query_params.get('paciente')
        is_active = self.request.query_params.get('is_active')

        if paciente:
            queryset = queryset.filter(paciente_id=paciente)

        if is_active is not None:
            queryset = queryset.filter(
                is_active=is_active.lower() == 'true'
            )

        return queryset