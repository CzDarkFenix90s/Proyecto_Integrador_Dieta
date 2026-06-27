from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('PACIENTE', 'Paciente'),
        ('NUTRICIONISTA', 'Nutricionista'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    address = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"