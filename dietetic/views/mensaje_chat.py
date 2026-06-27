from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from dietetic.models import MensajeChat
from dietetic.serializers.mensaje_chat import MensajeChatSerializer


class MensajeChatViewSet(viewsets.ModelViewSet):
    queryset = MensajeChat.objects.all().order_by("-id")
    serializer_class = MensajeChatSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = [
        "remitente",
        "destinatario",
        "leido",
    ]

    search_fields = [
        "contenido",
        "remitente__nombre",
        "destinatario__nombre",
    ]

    ordering_fields = [
        "id",
        "fecha_envio",
        "leido",
    ]

    ordering = [
        "-fecha_envio",
    ]

    def get_permissions(self):
        return [
            permissions.IsAuthenticated(),
        ]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        queryset = MensajeChat.objects.all()

        remitente = self.request.query_params.get("remitente")
        destinatario = self.request.query_params.get("destinatario")
        leido = self.request.query_params.get("leido")

        if remitente:
            queryset = queryset.filter(remitente=remitente)

        if destinatario:
            queryset = queryset.filter(destinatario=destinatario)

        if leido is not None:
            queryset = queryset.filter(leido=leido)

        return queryset.order_by("-fecha_envio", "-id")