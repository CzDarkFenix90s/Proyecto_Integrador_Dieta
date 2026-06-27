from rest_framework import viewsets
from dietetic.models import PerfilUsuario
from dietetic.serializers.perfil_usuario import PerfilUsuarioSerializer
from dietetic.permissions import IsStaffOrReadOnly
from dietetic.pagination import StandardPagination


class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.all()
    serializer_class = PerfilUsuarioSerializer
    pagination_class = StandardPagination

    filterset_fields = ['role']
    search_fields = [
        'user__username',
        'user__first_name',
        'user__last_name',
        'phone',
    ]

    permission_classes = [IsStaffOrReadOnly]