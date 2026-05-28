# dietetic/views/consulta_dietetica.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from dietetic.models import ConsultaDietetica
from dietetic.serializers.consulta_dietetica import ConsultaDieteticaSerializer
from dietetic.pagination import StandardPagination


class ConsultaDieteticaViewSet(viewsets.ModelViewSet):
    serializer_class   = ConsultaDieteticaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class   = StandardPagination
    filter_backends    = [DjangoFilterBackend, OrderingFilter]
    filterset_fields   = ['status', 'plan_nutricional', 'paciente', 'nutricionista']
    ordering_fields    = ['scheduled_time', 'created_at']
    ordering           = ['-scheduled_time']
    http_method_names  = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_queryset(self):
        return (
            ConsultaDietetica.objects
            .select_related('plan_nutricional', 'paciente', 'nutricionista')
            .all()
        )

    @action(detail=True, methods=['post'], url_path='add-session-note')
    def add_session_note(self, request, pk=None):
        consulta = self.get_object()
        if consulta.status not in ['programada', 'retrasada']:
            return Response(
                {'error': f'No se pueden agregar notas a una consulta con estado "{consulta.status}".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        notes = request.data.get('notes', '').strip()
        if not notes:
            return Response(
                {'error': 'Debe enviar un texto en notes.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        consulta.session_notes = notes
        consulta.save(update_fields=['session_notes'])
        return Response(ConsultaDieteticaSerializer(consulta).data)

    @action(detail=True, methods=['post'], url_path='start-consultation')
    def start_consultation(self, request, pk=None):
        consulta = self.get_object()
        if consulta.status != 'programada':
            return Response(
                {'error': 'Solo se pueden iniciar consultas programadas.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        consulta.status = 'en_curso'
        consulta.save(update_fields=['status'])
        return Response(ConsultaDieteticaSerializer(consulta).data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='update-status',
    )
    def update_status(self, request, pk=None):
        consulta       = self.get_object()
        new_status     = request.data.get('status')
        valid_statuses = [s[0] for s in ConsultaDietetica.STATUS_CHOICES]

        if new_status not in valid_statuses:
            return Response(
                {'error': f'Estado inválido. Opciones válidas: {valid_statuses}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        consulta.status = new_status
        consulta.save(update_fields=['status'])
        return Response(ConsultaDieteticaSerializer(consulta).data)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAdminUser],
        url_path='stats',
    )
    def stats(self, request):
        from django.db.models import Count
        qs = ConsultaDietetica.objects.all()
        by_status = {
            s: qs.filter(status=s).count()
            for s, _ in ConsultaDietetica.STATUS_CHOICES
        }
        return Response({
            'total_consultas': qs.count(),
            'by_status': by_status,
        })
