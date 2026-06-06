from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Q

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

    def get_queryset(self):
        user = self.request.user
        qs = ConsultaDietetica.objects.select_related(
            'plan_nutricional', 'paciente', 'nutricionista', 'paciente__user', 'nutricionista__user'
        )

        if user.is_staff or user.is_superuser:
            return qs.all()

        # Filtrar si el usuario es el paciente o el nutricionista de la cita
        return qs.filter(
            Q(paciente__user=user) | Q(nutricionista__user=user)
        ).distinct()

    @action(detail=False, methods=['get'], url_path='mine')
    def my_appointments(self, request):
        """
        Devuelve las consultas vinculadas al usuario logueado (como paciente o nutri).
        """
        qs = self.get_queryset()
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='add-session-note')
    def add_session_note(self, request, pk=None):
        consulta = self.get_object()
        
        # Solo el nutricionista asignado o un admin puede añadir notas
        if not request.user.is_staff and not (hasattr(consulta.nutricionista, 'user') and consulta.nutricionista.user == request.user):
            return Response({'error': 'No tienes permiso para añadir notas a esta consulta.'}, status=status.HTTP_403_FORBIDDEN)
            
        notes = request.data.get('notes', '').strip()
        if not notes:
            return Response({'error': 'Debe enviar un texto en notes.'}, status=status.HTTP_400_BAD_REQUEST)
            
        consulta.session_notes = notes
        consulta.save(update_fields=['session_notes'])
        return Response(self.get_serializer(consulta).data)

    @action(detail=True, methods=['post'], url_path='start-consultation')
    def start_consultation(self, request, pk=None):
        consulta = self.get_object()
        
        # Solo el nutricionista asignado o un admin puede iniciar la consulta
        if not request.user.is_staff and not (hasattr(consulta.nutricionista, 'user') and consulta.nutricionista.user == request.user):
            return Response({'error': 'No tienes permiso para iniciar esta consulta.'}, status=status.HTTP_403_FORBIDDEN)

        if consulta.status != 'programada':
            return Response({'error': 'Solo se pueden iniciar consultas en estado programada.'}, status=status.HTTP_400_BAD_REQUEST)
            
        consulta.status = 'en_curso'
        consulta.save(update_fields=['status'])
        return Response(self.get_serializer(consulta).data)

    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAdminUser],
        url_path='update-status',
    )
    def update_status(self, request, pk=None):
        consulta = self.get_object()
        new_status = request.data.get('status')
        
        valid_statuses = [choice[0] for choice in ConsultaDietetica.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response({'error': f'Estado inválido. Opciones válidas: {valid_statuses}'}, status=status.HTTP_400_BAD_REQUEST)
            
        consulta.status = new_status
        consulta.save(update_fields=['status'])
        return Response(self.get_serializer(consulta).data)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAdminUser],
        url_path='stats',
    )
    def stats(self, request):
        qs = self.get_queryset()
        
        status_counts = qs.values('status').annotate(count=Count('status'))
        
        by_status = {s: 0 for s, _ in ConsultaDietetica.STATUS_CHOICES}
        for item in status_counts:
            if item['status'] in by_status:
                by_status[item['status']] = item['count']
                
        return Response({
            'total_consultas': qs.count(),
            'by_status': by_status,
        })
