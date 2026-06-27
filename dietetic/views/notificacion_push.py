from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from dietetic.models import NotificacionPush
from dietetic.serializers.notificacion_push import NotificacionPushSerializer
from dietetic.permissions import IsStaffOrReadOnly


class NotificacionPushViewSet(viewsets.ModelViewSet):
    queryset = NotificacionPush.objects.all().order_by("-fecha_envio", "-id")
    serializer_class = NotificacionPushSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "paciente",
        "leido",
    ]

    search_fields = [
        "titulo",
        "mensaje",
    ]

    ordering_fields = [
        "fecha_envio",
        "titulo",
        "id",
    ]

    ordering = [
        "-fecha_envio",
    ]

    def get_permissions(self):
        if self.action in [
            "create",
            "destroy",
        ]:
            return [
                permissions.IsAuthenticated(),
                IsStaffOrReadOnly(),
            ]

        return [
            permissions.IsAuthenticated(),
        ]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = NotificacionPush.objects.all()

        paciente = self.request.query_params.get("paciente")
        leido = self.request.query_params.get("leido")

        if paciente:
            queryset = queryset.filter(paciente=paciente)

        if leido is not None:
            queryset = queryset.filter(leido=leido)

        return queryset.order_by("-fecha_envio", "-id")